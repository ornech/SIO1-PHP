#!/usr/bin/env python3
"""Génère et vérifie les PDF du cours : un PDF par chapitre.

Un chapitre est un dossier « NN-sujet/ » qui contient un README.md et, au besoin, un dossier images/.
Chaque PDF contient : une page de titre, un sommaire cliquable avec numéros de page, des signets
(volet de navigation du lecteur PDF), des liens internes fonctionnels, le code coloré et les encadrés.

Usage :
    python3 outils/pdf.py generer  [dossier_du_depot] [dossier_de_sortie]   (défaut : . et pdf/)
    python3 outils/pdf.py verifier [dossier_du_depot] [dossier_des_pdf]     (défaut : . et pdf/)

Dépendances : pip install weasyprint==70.0 markdown-it-py==4.2.0 Pygments==2.21.0 pypdf==7.0.0
Sous Linux, WeasyPrint demande aussi Pango et des polices : voir .github/workflows/pdf.yml.

« generer » ÉCHOUE (code de sortie 1) si un lien interne, un lien vers un autre chapitre ou une image est cassé.
« verifier » échoue (code de sortie 1) si un PDF ne respecte pas les contrôles listés dans verifier().

Le numéro de version de la page de garde est le dernier tag Git « vX.Y » (le tag « pdf-latest » de la release
est ignoré) :  git tag -a v1.0 -m "Première version du cours" && git push origin v1.0
Les versions de référence de la page de garde sont lues dans le bloc « Versions de référence » du README racine.
"""
import re, sys, html, datetime, pathlib, subprocess, unicodedata, logging, warnings
from urllib.parse import unquote  # markdown-it encode les accents des liens (é -> %C3%A9)

# Page de garde et propriétés des PDF (auteur, sujet, mots-clés…).
META = {
    "auteur": {"nom": "Jean-François ORNECH", "fonction": "Enseignant"},
    "document": {
        "serie": "Introduction à PHP",
        "public": "BTS SIO, 1ʳᵉ année (tronc commun SISR et SLAM)",
        "depot": "https://github.com/ornech/SIO1-PHP",
        "mots_cles": "PHP, programmation, variables, tableaux, boucles, fonctions, formulaires, débutants, BTS SIO, SISR, SLAM",
    },
    "licence": {
        "nom": "CC BY-NC-SA 4.0",
        "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr",
        "resume": "Attribution, pas d'utilisation commerciale, partage dans les mêmes conditions",
    },

}
GITHUB = META["document"]["depot"] + "/blob/main/"


# ---------------------------------------------------------------- informations communes

def _git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def infos_git(repo):
    """Commit, date et version du dépôt. La version est le dernier tag « vX.Y » : le tag
    « pdf-latest » de la release est volontairement ignoré (--match 'v[0-9]*')."""
    tag = _git(repo, "describe", "--tags", "--match", "v[0-9]*", "--abbrev=0")
    distance = int(_git(repo, "rev-list", "--count", f"{tag}..HEAD") or 0) if tag else 0
    return {
        "sha": _git(repo, "rev-parse", "HEAD"),
        "court": _git(repo, "rev-parse", "--short=7", "HEAD") or "inconnu",
        "date_iso": _git(repo, "show", "-s", "--format=%cI", "HEAD"),
        "date_fr": _git(repo, "show", "-s", "--format=%cd", "--date=format:%d/%m/%Y", "HEAD"),
        "tag": tag,
        "distance": distance,
        "modifie": bool(_git(repo, "status", "--porcelain", "--untracked-files=no")),  # seulement hors CI
    }


def libelle_version(g):
    """Texte complet de la version, pour la page de garde."""
    if not g["tag"]:
        return "non numérotée (aucun tag de version pour l'instant)"
    if g["distance"] == 0:
        return g["tag"]
    s = "s" if g["distance"] > 1 else ""
    return f"{g['tag']} + {g['distance']} commit{s}"


def version_courte(g):
    """Version compacte, pour le pied de page."""
    if not g["tag"]:
        return ""
    return g["tag"] if g["distance"] == 0 else f"{g['tag']}+{g['distance']}"


def versions_reference(repo):
    """Versions de référence lues dans le README racine (une seule source de vérité)."""
    txt = (pathlib.Path(repo) / "README.md").read_text(encoding="utf-8")
    bloc = txt.split("Versions de référence", 1)[1]
    return [f"{nom} {ver}" for nom, ver in re.findall(r"^- (.+?) : (\S+)\s*$", bloc, re.M)]


def sans_code(texte):
    """Texte markdown sans les blocs de code (un « # commentaire » shell n'est pas un titre)."""
    return re.sub(r"^```.*?^```", "", texte, flags=re.S | re.M)


def chapitres(repo):
    """Chapitres du cours : dossiers « NN-sujet/ » contenant un README.md, dans l'ordre des numéros.
    Retourne {nom_du_dossier: titre}, le titre étant le premier titre de niveau 1 du README.md."""
    out = {}
    for f in sorted(pathlib.Path(repo).glob("[0-9][0-9]-*/README.md")):
        m = re.search(r"^# (.+)$", sans_code(f.read_text(encoding="utf-8")), re.M)
        out[f.parent.name] = re.sub(r"[*`]", "", m.group(1)).strip() if m else f.parent.name
    return out


def fold(text):
    """Identifiant ASCII stable (sans accents) pour les ancres."""
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\- ]", "", t.lower()).strip().replace(" ", "-")
    return re.sub(r"-+", "-", t) or "section"


# ---------------------------------------------------------------- génération

CSS_TEXTE = """
@page { size: A4; margin: 20mm 17mm 20mm 17mm;
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 8pt; color: #666; }
  @bottom-left { content: "__PIED__"; font-size: 8pt; color: #666; }
  @top-right { content: string(chapitre); font-size: 8pt; color: #666; } }
@page :first { @top-right { content: none; } @bottom-center { content: none; } @bottom-left { content: none; } }
html { font-family: "Liberation Sans", "DejaVu Sans", sans-serif; font-size: 10pt; line-height: 1.45; color: #1f2328; }
h1 { font-size: 20pt; margin: 0 0 10pt; border-bottom: 2px solid #d0d7de; padding-bottom: 4pt; string-set: chapitre content(text); }
h2 { font-size: 14pt; margin: 16pt 0 6pt; border-bottom: 1px solid #d0d7de; padding-bottom: 2pt; }
h3 { font-size: 12pt; margin: 12pt 0 4pt; } h1, h2, h3 { break-after: avoid; }
p { margin: 5pt 0; } a { color: #0969da; text-decoration: none; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.5pt; background: #eff1f3; padding: 0 2pt; border-radius: 2pt; }
pre.code { white-space: pre-wrap; overflow-wrap: anywhere; background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 4pt; padding: 6pt 8pt; font-size: 8pt; line-height: 1.35; margin: 6pt 0; }
pre.code code { background: none; padding: 0; font-size: 8pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9pt; }
th, td { border: 1px solid #d0d7de; padding: 3pt 5pt; vertical-align: top; } th { background: #f6f8fa; } tr { break-inside: avoid; }
blockquote { margin: 8pt 0; padding: 4pt 10pt; border-left: 4pt solid #d0d7de; color: #444; }
blockquote.alert { background: #f6f8fa; break-inside: avoid; color: #1f2328; }
blockquote.note { border-left-color: #0969da; background: #ddf4ff; } blockquote.warning { border-left-color: #bf8700; background: #fff8c5; }
.alert-titre { font-weight: bold; margin: 2pt 0; } blockquote.note .alert-titre { color: #0969da; } blockquote.warning .alert-titre { color: #9a6700; }
img { max-width: 100%; }
.chapitre { break-before: page; } .couverture { padding-top: 28mm; }
.serie { color: #57606a; font-size: 12pt; margin: 0 0 4pt; text-transform: uppercase; letter-spacing: 1pt; }
.titre-doc { font-size: 27pt; border: none; string-set: none; margin: 0 0 16mm; }
table.infos { width: 100%; font-size: 10pt; margin: 0 0 8mm; }
table.infos th { width: 33%; text-align: left; background: #f6f8fa; } .couverture blockquote.alert { font-size: 9.5pt; }
.date { color: #666; margin-top: 12mm; font-size: 9pt; }
.sommaire { break-before: page; } nav.toc ul { list-style: none; padding: 0; margin: 0; }
nav.toc li { margin: 2pt 0; } nav.toc li.niv1 { margin-top: 8pt; font-weight: bold; } nav.toc li.niv2 { margin-left: 14pt; font-size: 9pt; }
nav.toc a { color: #1f2328; } nav.toc a::after { content: leader('.') target-counter(attr(href), page); font-weight: normal; }
ul, ol { margin: 4pt 0; padding-left: 18pt; } li { margin: 1pt 0; }
"""


def inline_text(tok):
    return "".join(c.content for c in (tok.children or []) if c.type in ("text", "code_inline"))


def convertir(repo, tp, titre_tp, git, versions, liens_absents):
    """Markdown d'un chapitre -> document HTML (page de titre, sommaire, contenu)."""
    from markdown_it import MarkdownIt
    from pygments import highlight as pyg_highlight
    from pygments.lexers import get_lexer_by_name, TextLexer
    from pygments.formatters import HtmlFormatter

    def hl(code, lang, attrs):
        try:
            if lang == "php":  # un extrait sans « <?php » est du PHP, pas du texte autour d'un script
                lexer = get_lexer_by_name("php", startinline="<?" not in code)
            else:
                lexer = get_lexer_by_name(lang) if lang else TextLexer()
        except Exception:
            lexer = TextLexer()
        body = pyg_highlight(code, lexer, HtmlFormatter(nowrap=True))
        return f'<pre class="code"><code>{body}</code></pre>'

    d = repo / tp
    files = [d / "README.md"]
    ids = {f.name: "ch-" + fold(f.stem) for f in files}  # README.md -> ch-readme
    md = MarkdownIt("commonmark", {"html": False, "highlight": hl}).enable("table").enable("strikethrough")
    corps_chapitres, toc, liens_externes = [], [], 0

    for f in files:
        fid = ids[f.name]
        tokens = md.parse(f.read_text(encoding="utf-8"))
        if f.name == "README.md":  # un éventuel « Sommaire » du README est remplacé par le sommaire généré
            debut = next((k for k, t in enumerate(tokens) if t.type == "heading_open"
                          and inline_text(tokens[k + 1]) == "Sommaire"), None)
            if debut is not None:
                fin = next((k for k in range(debut + 1, len(tokens)) if tokens[k].type == "heading_open"), len(tokens))
                del tokens[debut:fin]
        vus, premier_h1 = {}, True
        i = 0
        while i < len(tokens):
            t = tokens[i]
            # ---- titres : identifiants uniques par fichier, un seul H1 par chapitre
            if t.type == "heading_open":
                niveau = int(t.tag[1])
                texte = inline_text(tokens[i + 1])
                if niveau == 1 and premier_h1:
                    t.attrSet("id", fid); premier_h1 = False
                    toc.append((1, texte, fid))
                else:
                    if niveau == 1:
                        niveau = 2; t.tag = "h2"; tokens[i + 2].tag = "h2"
                    base = f"{fid}-{fold(texte)}"
                    n = vus.get(base, 0); vus[base] = n + 1
                    ident = base if n == 0 else f"{base}-{n}"
                    t.attrSet("id", ident)
                    if niveau == 2:
                        toc.append((2, texte, ident))
            # ---- encadrés GitHub : > [!NOTE] / > [!WARNING]
            if t.type == "blockquote_open" and tokens[i + 1].type == "paragraph_open":
                inl = tokens[i + 2]
                m = re.match(r"\[!(NOTE|WARNING)\]\s*", inl.content)
                if m:
                    genre = m.group(1).lower()
                    t.attrSet("class", f"alert {genre}")
                    t.attrSet("data-titre", "Note" if genre == "note" else "Attention")
                    ch = inl.children
                    while ch and (ch[0].type == "softbreak" or "[!" in ch[0].content or ch[0].content.strip() == ""):
                        ch.pop(0)
                        if ch and ch[0].type == "softbreak": ch.pop(0); break
                    inl.content = inl.content[m.end():]
            # ---- liens et images
            if t.type == "inline":
                for c in t.children:
                    if c.type == "link_open":
                        href = c.attrGet("href") or ""
                        if href.startswith("#"):
                            c.attrSet("href", "#" + fid + "-" + fold(unquote(href[1:])))
                        elif re.match(r"https?://", href):
                            liens_externes += 1
                        else:
                            chemin, _, ancre = unquote(href).partition("#")
                            cible = (d / chemin).resolve()
                            if cible.parent == d.resolve() and cible.name in ids:
                                c.attrSet("href", "#" + ids[cible.name] + (("-" + fold(ancre)) if ancre else ""))
                            elif cible.suffix == ".md":  # autre chapitre : lien vers GitHub
                                if not cible.exists():
                                    liens_absents.append(f"{tp} : lien vers un fichier absent : {href}")
                                c.attrSet("href", GITHUB + str(cible.relative_to(repo)))
                                liens_externes += 1
                    elif c.type == "image":
                        c.attrSet("src", (d / unquote(c.attrGet("src"))).resolve().as_uri())
            i += 1
        corps = md.renderer.render(tokens, md.options, {})
        # étiquette d'encadré (Note / Attention) insérée devant le contenu
        corps = re.sub(r'<blockquote class="alert (note|warning)" data-titre="([^"]+)">',
                       lambda m: f'<blockquote class="alert {m.group(1)}"><p class="alert-titre">{m.group(2)}</p>', corps)
        corps_chapitres.append(f'<section class="chapitre">{corps}</section>')

    sommaire = "".join(
        f'<li class="niv{n}"><a href="#{ident}">{html.escape(txt)}</a></li>' for n, txt, ident in toc
    )
    e = html.escape
    aut, doc_m, lic = META["auteur"], META["document"], META["licence"]
    version = libelle_version(git) + (" (modifications locales non commitées)" if git["modifie"] else "")
    lien_commit = f'{doc_m["depot"]}/commit/{git["sha"]}' if git["sha"] else doc_m["depot"]
    ligne = lambda k, v: f"<tr><th>{k}</th><td>{v}</td></tr>"
    infos = "".join([
        ligne("Auteur", f'{e(aut["nom"])}, {e(aut["fonction"].lower())}'),
        ligne("Public visé", e(doc_m["public"])),
        ligne("Version", e(version)),
        ligne("Commit", f'<a href="{e(lien_commit)}">{e(git["court"])}</a>, le {e(git["date_fr"])}'),
        ligne("Versions de référence", e(" · ".join(versions))),
        ligne("Dépôt", f'<a href="{e(doc_m["depot"])}">{e(doc_m["depot"])}</a>'),
        ligne("Licence", f'<a href="{e(lic["url"])}">{e(lic["nom"])}</a> : {e(lic["resume"])}'),
    ])
    date = datetime.date.today().strftime("%d/%m/%Y")
    description = f"{titre_tp}" + (f". Version {git['tag']}" if git["tag"] and git["distance"] == 0 else "") + f". Commit {git['court']}, {git['date_fr']}."
    metas = f"""<meta name="author" content="{e(aut['nom'])}">
<meta name="description" content="{e(description)}">
<meta name="keywords" content="{e(doc_m['mots_cles'])}">
<meta name="generator" content="WeasyPrint, outils/pdf.py (commit {e(git['court'])})">
<meta name="dcterms.created" content="{e(git['date_iso'])}">"""
    doc = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{e(titre_tp)}</title>
{metas}</head><body>
<section class="couverture"><p class="serie">{e(doc_m["serie"])}</p>
<h1 class="titre-doc" style="bookmark-level:none">{e(titre_tp)}</h1>
<table class="infos">{infos}</table>
<p class="date">PDF généré le {date}</p></section>
<section class="sommaire"><h1 style="bookmark-level:none">Sommaire</h1><nav class="toc"><ul>{sommaire}</ul></nav></section>
{''.join(corps_chapitres)}
</body></html>"""
    return doc, d, liens_externes


def generer(repo, out):
    from pygments.formatters import HtmlFormatter
    from weasyprint import HTML, CSS

    class Collecteur(logging.Handler):
        """Conserve les avertissements de WeasyPrint (ancres introuvables, images manquantes…)."""
        def __init__(self):
            super().__init__(); self.messages = []
        def emit(self, record):
            self.messages.append(record.getMessage())

    collecteur, liens_absents = Collecteur(), []  # liens_absents : liens vers un autre chapitre dont le fichier n'existe pas
    logging.getLogger("weasyprint").addHandler(collecteur)
    logging.getLogger("weasyprint").setLevel(logging.WARNING)

    liste = chapitres(repo)
    if not liste:
        sys.exit("ERREUR : aucun chapitre trouvé (dossier « NN-sujet/ » contenant un README.md).")
    out.mkdir(parents=True, exist_ok=True)
    pyg_css = HtmlFormatter().get_style_defs("pre.code")
    git, versions = infos_git(repo), versions_reference(repo)
    print(f"version : {libelle_version(git)} · commit {git['court']} · {git['date_fr']}")
    for tp, titre in liste.items():
        doc, base, ext = convertir(repo, tp, titre, git, versions, liens_absents)
        pdf = out / f"{tp}.pdf"
        court = f"Chapitre {int(tp[:2])}"  # « Chapitre 3 »
        pied = " · ".join(x for x in (court, version_courte(git), git["court"]) if x)
        css = CSS_TEXTE.replace("__PIED__", pied.replace("\\", "\\\\").replace('"', '\\"'))
        HTML(string=doc, base_url=str(base) + "/").write_pdf(str(pdf), stylesheets=[CSS(string=css + pyg_css)])
        print(f"{pdf}  ({pdf.stat().st_size // 1024} Ko, {ext} lien(s) externe(s))")
    graves = [m for m in collecteur.messages if re.search(r"anchor|image|failed|not found|URL", m, re.I)] + liens_absents
    for m in collecteur.messages:
        if m not in graves:
            print("avertissement :", m)
    if graves:
        print("\nERREUR : liens ou images cassés :", *graves, sep="\n  - ")
        sys.exit(1)


# ---------------------------------------------------------------- vérification

def verifier(repo, pdfs):
    """Garde-fou : signets, liens internes, contenu interdit, images, propriétés du PDF, page de garde."""
    from pypdf import PdfReader
    warnings.filterwarnings("ignore")

    liste, git, erreurs = chapitres(repo), infos_git(repo), []
    interdits = ["[!NOTE]", "[!WARNING]"]  # un marqueur d'encadré visible dans le PDF = encadré non converti
    normaliser = lambda t: " ".join(t.split())
    ko = lambda tp, msg: erreurs.append(f"{tp}: {msg}")
    if not liste:
        erreurs.append("aucun chapitre trouvé (dossier « NN-sujet/ » contenant un README.md)")

    for tp, titre in liste.items():
        texte_md = sans_code((repo / tp / "README.md").read_text(encoding="utf-8"))
        pdf = pdfs / f"{tp}.pdf"
        if not pdf.exists():
            ko(tp, "PDF absent"); continue
        r = PdfReader(str(pdf))
        pages = len(r.pages)
        if pages < 3:  # page de titre, sommaire, au moins une page de contenu
            ko(tp, f"seulement {pages} page(s)")

        # --- signets (volet de navigation) : le titre du chapitre (premier H1 du README.md)
        titres = []
        def parcourir(noeuds):
            for x in noeuds:
                if isinstance(x, list): parcourir(x)
                else: titres.append(x.title)
        parcourir(r.outline)
        if titre not in titres:
            ko(tp, f"signet manquant : « {titre} »")

        # --- liens internes : chaque lien doit pointer vers une page existante
        internes = 0
        for pg in r.pages:
            for a in pg.get("/Annots", []) or []:
                a = a.get_object()
                if a.get("/Subtype") != "/Link": continue
                dest = a.get("/Dest") or (a.get("/A", {}).get("/D") if a.get("/A", {}).get("/S") == "/GoTo" else None)
                if dest is None: continue
                internes += 1
                try:
                    if isinstance(dest, str):
                        dest = r.named_destinations[dest]
                        num = r.get_destination_page_number(dest)
                    else:
                        num = r.get_page_number(dest[0].get_object())
                    if not (0 <= num < pages): raise ValueError
                except Exception:
                    ko(tp, "lien interne vers une destination introuvable")
        # chaque entrée du sommaire (premier H1 et chaque H2) est un lien interne
        entrees = len(re.findall(r"^#{1,2} \S", texte_md, re.M))
        if internes < entrees:
            ko(tp, f"trop peu de liens internes ({internes}, {entrees} entrée(s) au sommaire)")

        # --- contenu interdit
        texte = "\n".join(p.extract_text() for p in r.pages)
        for mot in interdits:
            if mot.lower() in texte.lower():
                ko(tp, f"contenu interdit dans le PDF : « {mot} »")

        # --- images : WeasyPrint les déclare dans les ressources de chaque page, on compte les images DISTINCTES
        imgs = len({im.name for p in r.pages for im in p.images})
        attendues = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", texte_md))
        if imgs < attendues:
            ko(tp, f"{imgs} image(s) dans le PDF, {attendues} attendue(s)")

        # --- propriétés du PDF (auteur, titre, sujet, mots-clés)
        props = r.metadata or {}
        if props.get("/Author") != META["auteur"]["nom"]:
            ko(tp, f"propriété Auteur incorrecte : {props.get('/Author')!r}")
        for cle in ("/Title", "/Subject", "/Keywords"):
            if not props.get(cle):
                ko(tp, f"propriété {cle[1:]} vide")

        # --- page de garde : auteur, licence, commit (et version si un tag existe)
        garde = normaliser(r.pages[0].extract_text())
        attendus = [META["auteur"]["nom"], META["licence"]["nom"], git["court"]]
        if git["tag"]:
            attendus.append(git["tag"])
        for a in attendus:
            if a not in garde:
                ko(tp, f"page de garde : « {a[:50]}… » introuvable")
        # --- pied de page : le commit figure sur les pages courantes
        if git["court"] not in normaliser(r.pages[1].extract_text()):
            ko(tp, "pied de page : commit absent")

        print(f"{tp}.pdf : {pages} pages, {len(titres)} signets, {internes} liens internes, {imgs} image(s)")

    if erreurs:
        print("\nÉCHEC :", *erreurs, sep="\n  - ")
        sys.exit(1)
    print("Vérification des PDF : OK")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("generer", "verifier"):
        sys.exit(__doc__)
    depot = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else ".").resolve()
    dossier = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else depot / "pdf").resolve()
    (generer if sys.argv[1] == "generer" else verifier)(depot, dossier)
