# TP : les notes des étudiants (fichier JSON)

À la fin de ce TP, vous saurez :

- écrire et lire des données au format JSON avec `json_encode()` et `json_decode()` ;
- convertir un fichier CSV en fichier JSON ;
- adapter des pages PHP à une nouvelle source de données ;
- enregistrer les modifications d'un formulaire dans un fichier avec `file_put_contents()` ;
- lire l'avertissement « Permission denied » et tester le résultat d'une écriture.

Prérequis : le chapitre 10 et ses fichiers `data.csv`, `liste.php` et `etudiant.php`. Créez un dossier `tp11` dans la racine du serveur (`/var/www/html` sous Linux), copiez-y `data.csv`, et placez votre terminal dedans.

Ce TP reprend l'application du chapitre 10 avec une autre source de données : un fichier JSON, plus lisible qu'un fichier CSV, qui peut aussi être réécrit par un formulaire.

## Le format JSON

**JSON** est un format texte pour écrire des données. Un tableau associatif s'écrit entre accolades `{ }`, sous la forme `"clé":valeur`. Un tableau indexé s'écrit entre crochets `[ ]`. La fonction `json_encode()` transforme un tableau PHP en texte JSON. Créez un fichier `json.php` :

```php
<?php
$etudiant = ["prenom" => "Gabriel", "nom" => "Moore", "notes" => [16, 13, 14]];
echo json_encode($etudiant), "\n";
?>
```

**Prédisez** le texte JSON, puis exécutez `php json.php`.

Vous devez voir :

```text
{"prenom":"Gabriel","nom":"Moore","notes":[16,13,14]}
```

**Modifiez une seule chose.** Remplacez le tableau de la ligne 2 par `["prenom" => "Léo", "notes" => [20, 1, 8]]`. Ce changement ajoute un caractère accentué.

```php
<?php
$etudiant = ["prenom" => "Léo", "notes" => [20, 1, 8]];
echo json_encode($etudiant), "\n";
?>
```

**Prédisez** : l'accent est-il conservé ? Exécutez le script.

Vous devez voir :

```text
{"prenom":"L\u00e9o","notes":[20,1,8]}
```

`\u00e9` est le code du caractère `é` : c'est du JSON valide, mais peu lisible.

**Modifiez une seule chose.** Ligne 3, ajoutez un second argument à `json_encode()` : `JSON_UNESCAPED_UNICODE`. Cette option demande à PHP de ne pas remplacer les caractères accentués par des codes.

```php
<?php
$etudiant = ["prenom" => "Léo", "notes" => [20, 1, 8]];
echo json_encode($etudiant, JSON_UNESCAPED_UNICODE), "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
{"prenom":"Léo","notes":[20,1,8]}
```

La fonction `json_decode()` fait l'inverse : elle transforme un texte JSON en tableau PHP, à condition de lui donner `true` comme second argument. Créez un fichier `decoder.php` :

```php
<?php
$json = '{"prenom":"Gabriel","nom":"Moore","notes":[16,13,14]}';
$etudiant = json_decode($json, true);
echo $etudiant["prenom"], " ", $etudiant["notes"][2], "\n";
?>
```

**Prédisez** la ligne affichée, puis exécutez `php decoder.php`.

Vous devez voir :

```text
Gabriel 14
```

## Convertir le fichier CSV en fichier JSON

Plutôt que de télécharger un fichier JSON, vous allez le fabriquer à partir de `data.csv`. Créez un fichier `convertir.php` :

```php
<?php
$lignes = array_map('str_getcsv', file('data.csv'));
$etudiants = [];
foreach ($lignes as $ligne) {
    $etudiants[] = [
        "prenom" => $ligne[0],
        "nom" => $ligne[1],
        "notes" => [(int) $ligne[2], (int) $ligne[3], (int) $ligne[4]],
    ];
}
file_put_contents('data.json', json_encode($etudiants, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
echo count($etudiants), " étudiants écrits\n";
?>
```

- Ligne 2 : lit le CSV, comme au chapitre 10.
- Lignes 4 à 10 : construisent, pour chaque ligne du CSV, un tableau associatif avec les clés `prenom`, `nom` et `notes`. Le mot `(int)` placé devant une valeur la convertit en entier : sans lui, les notes seraient écrites comme du texte, `"16"`, et non comme des nombres, `16`.
- Ligne 11 : `json_encode()` transforme tout le tableau en JSON. L'option `JSON_PRETTY_PRINT` ajoute des retours à la ligne et des retraits pour que le fichier soit lisible. `file_put_contents()` écrit ce texte dans le fichier `data.json`, qu'il crée s'il n'existe pas.

**Prédisez** le message affiché, puis exécutez la commande :

```bash
php convertir.php
```

Vous devez voir :

```text
20 étudiants écrits
```

Affichez le début du fichier créé. Sous Windows, ouvrez `data.json` dans un éditeur de texte à la place.

```bash
head -n 12 data.json
```

Vous devez voir :

```text
[
    {
        "prenom": "Gabriel",
        "nom": "Moore",
        "notes": [
            16,
            13,
            14
        ]
    },
    {
        "prenom": "Léo",
```

## Lire le fichier JSON dans les pages

Il faut maintenant que les pages du chapitre 10 lisent `data.json`. Trois changements sont nécessaires dans chaque page : la ligne qui lit les données, puis l'accès au nom, au prénom (`$etudiant["nom"]`, `$etudiant["prenom"]`) et aux notes (`$etudiant["notes"][$i]`).

Dans `tp11`, créez un fichier `liste.php` :

```php
<?php
$data = json_decode(file_get_contents('data.json'), true);
$moyennes = [0, 0, 0];
foreach ($data as $etudiant) {
    for ($i = 0; $i < 3; $i++) {
        $moyennes[$i] += $etudiant["notes"][$i];
    }
}
foreach ($moyennes as $i => $total) {
    $moyennes[$i] = round($total / count($data), 2);
}
echo "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n</head>\n<body>\n";
echo "<table border='1'>\n";
echo "<tr><th>Nom</th><th>Prénom</th><th>Épreuve 1</th><th>Moyenne 1</th><th>Épreuve 2</th><th>Moyenne 2</th><th>Épreuve 3</th><th>Moyenne 3</th></tr>\n";
foreach ($data as $numero => $etudiant) {
    echo "<tr><td><a href='etudiant.php?id=$numero'>{$etudiant["nom"]}</a></td><td>{$etudiant["prenom"]}</td>";
    for ($i = 0; $i < 3; $i++) {
        echo "<td>", $etudiant["notes"][$i], "</td><td>", $moyennes[$i], "</td>";
    }
    echo "</tr>\n";
}
echo "</table>\n</body>\n</html>\n";
?>
```

La ligne 2 lit le contenu du fichier avec `file_get_contents()`, puis le convertit avec `json_decode()`. Dans une chaîne entre guillemets doubles, les accolades de `{$etudiant["nom"]}` délimitent l'expression à remplacer par sa valeur.

Créez un fichier `etudiant.php` :

```php
<?php
$data = json_decode(file_get_contents('data.json'), true);
$id = $_GET["id"] ?? "";
if (!isset($data[$id])) {
    echo "Étudiant introuvable\n";
} else {
    $e = $data[$id];
    echo "<h1>", htmlspecialchars($e["nom"]), " ", htmlspecialchars($e["prenom"]), "</h1>\n";
    echo "<ul>\n";
    for ($i = 0; $i < 3; $i++) {
        echo "<li>Épreuve ", $i + 1, " : ", $e["notes"][$i], "</li>\n";
    }
    echo "</ul>\n";
}
?>
```

**Prédisez** : les pages vont-elles afficher les mêmes résultats qu'au chapitre 10 ? Exécutez la commande suivante, puis affichez la fiche de l'étudiant 1.

```bash
curl -s http://localhost/tp11/liste.php | sed -n "7,10p"
```

Vous devez voir :

```text
<table border='1'>
<tr><th>Nom</th><th>Prénom</th><th>Épreuve 1</th><th>Moyenne 1</th><th>Épreuve 2</th><th>Moyenne 2</th><th>Épreuve 3</th><th>Moyenne 3</th></tr>
<tr><td><a href='etudiant.php?id=0'>Moore</a></td><td>Gabriel</td><td>16</td><td>11.8</td><td>13</td><td>10.65</td><td>14</td><td>11.3</td></tr>
<tr><td><a href='etudiant.php?id=1'>Bidelspach</a></td><td>Léo</td><td>20</td><td>11.8</td><td>1</td><td>10.65</td><td>8</td><td>11.3</td></tr>
```

```bash
curl -s "http://localhost/tp11/etudiant.php?id=1"
```

Vous devez voir :

```text
<h1>Bidelspach Léo</h1>
<ul>
<li>Épreuve 1 : 20</li>
<li>Épreuve 2 : 1</li>
<li>Épreuve 3 : 8</li>
</ul>
```

Les résultats sont identiques : seule la source de données a changé.

## Modifier un dossier avec un formulaire

Créez un fichier `modifier.php`. Selon la situation, il affiche le formulaire de modification (sans données envoyées), enregistre les données reçues (par POST), ou signale que l'étudiant n'existe pas :

```php
<?php
$data = json_decode(file_get_contents('data.json'), true);
$id = $_GET["id"] ?? "";
if (!isset($data[$id])) {
    echo "Étudiant introuvable\n";
} elseif (isset($_POST["nom"])) {
    $data[$id]["prenom"] = $_POST["prenom"];
    $data[$id]["nom"] = $_POST["nom"];
    $data[$id]["notes"] = [(int) $_POST["note1"], (int) $_POST["note2"], (int) $_POST["note3"]];
    file_put_contents('data.json', json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo "Dossier enregistré\n";
} else {
    $e = $data[$id];
    $prenom = htmlspecialchars($e["prenom"]);
    $nom = htmlspecialchars($e["nom"]);
    echo "<form action='modifier.php?id=$id' method='POST'>\n";
    echo "<input name='prenom' value='$prenom'>\n";
    echo "<input name='nom' value='$nom'>\n";
    for ($i = 0; $i < 3; $i++) {
        $numero = $i + 1;
        echo "<input name='note$numero' value='{$e["notes"][$i]}'>\n";
    }
    echo "<input type='submit' value='Enregistrer'>\n";
    echo "</form>\n";
}
?>
```

- Ligne 6 : `isset($_POST["nom"])` est vrai quand un formulaire a été envoyé par POST.
- Lignes 7 à 10 : remplacent les données de l'étudiant `$id` par celles du formulaire, puis réécrivent tout le fichier `data.json`.
- Lignes 12 à 23 : affichent le formulaire. L'attribut `value` de chaque champ contient la valeur actuelle, pour que le formulaire apparaisse déjà rempli.

**Prédisez** les champs du formulaire de l'étudiant 0, puis exécutez la commande :

```bash
curl -s "http://localhost/tp11/modifier.php?id=0"
```

Vous devez voir :

```text
<form action='modifier.php?id=0' method='POST'>
<input name='prenom' value='Gabriel'>
<input name='nom' value='Moore'>
<input name='note1' value='16'>
<input name='note2' value='13'>
<input name='note3' value='14'>
<input type='submit' value='Enregistrer'>
</form>
```

**Modifiez une seule chose.** Envoyez des données par POST, comme le ferait le formulaire : nom `Moore-Dupont` et note 3 égale à 15.

```bash
curl -s -d "prenom=Gabriel&nom=Moore-Dupont&note1=16&note2=13&note3=15" "http://localhost/tp11/modifier.php?id=0"
```

**Prédisez** le message affiché, puis exécutez la commande.

Vous devez voir :

```text
Dossier enregistré
```

Vérifiez que la fiche a changé :

```bash
curl -s "http://localhost/tp11/etudiant.php?id=0"
```

Vous devez voir :

```text
<h1>Moore-Dupont Gabriel</h1>
<ul>
<li>Épreuve 1 : 16</li>
<li>Épreuve 2 : 13</li>
<li>Épreuve 3 : 15</li>
</ul>
```

## Lire l'avertissement « Permission denied »

Pour écrire dans un fichier, PHP doit en avoir le droit. Sous Linux, retirez à tous les utilisateurs le droit d'écrire dans `data.json` :

```bash
chmod a-w data.json
```

**Prédisez** ce que la page va répondre à un nouvel envoi de données, puis exécutez la commande :

```bash
curl -s -d "prenom=Gabriel&nom=Moore&note1=16&note2=13&note3=14" "http://localhost/tp11/modifier.php?id=0"
```

Vous devez voir :

```text
Dossier enregistré
```

La page répond que le dossier est enregistré, alors que ce n'est pas vrai. Cherchez la cause dans le journal d'erreurs d'Apache :

```bash
sudo grep -o "PHP Warning:.*" /var/log/apache2/error.log | tail -1
```

Vous devez voir :

```text
PHP Warning:  file_put_contents(data.json): Failed to open stream: Permission denied in /var/www/html/tp11/modifier.php on line 10
```

Lisez le message :

- `file_put_contents(data.json): Failed to open stream: Permission denied` : PHP n'a pas pu ouvrir `data.json` pour y écrire, faute de droit.
- `in /var/www/html/tp11/modifier.php on line 10` : le fichier et la ligne de l'écriture.

Apache s'exécute avec son propre compte utilisateur, souvent différent du vôtre (par exemple `www-data` sous Debian et Ubuntu). Le même avertissement apparaît si ce compte n'a pas le droit d'écrire dans `data.json` : il faut alors lui donner ce droit, par exemple avec `sudo chown www-data data.json` sous Debian et Ubuntu.

> [!WARNING]
> Journal et configuration
>
> L'emplacement du journal et l'affichage des messages dépendent du système et de la configuration de PHP (`php.ini`). Ces messages viennent de PHP 8.4.27.

**Modifiez une seule chose.** Dans `modifier.php`, remplacez la ligne 10 `file_put_contents(…);` et la ligne 11 `echo "Dossier enregistré\n";` par un test du résultat. La fonction `file_put_contents()` renvoie `false` quand l'écriture échoue.

```php
<?php
$data = json_decode(file_get_contents('data.json'), true);
$id = $_GET["id"] ?? "";
if (!isset($data[$id])) {
    echo "Étudiant introuvable\n";
} elseif (isset($_POST["nom"])) {
    $data[$id]["prenom"] = $_POST["prenom"];
    $data[$id]["nom"] = $_POST["nom"];
    $data[$id]["notes"] = [(int) $_POST["note1"], (int) $_POST["note2"], (int) $_POST["note3"]];
    $ecrit = file_put_contents('data.json', json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    if ($ecrit === false) {
        echo "Erreur : enregistrement impossible\n";
    } else {
        echo "Dossier enregistré\n";
    }
} else {
    $e = $data[$id];
    $prenom = htmlspecialchars($e["prenom"]);
    $nom = htmlspecialchars($e["nom"]);
    echo "<form action='modifier.php?id=$id' method='POST'>\n";
    echo "<input name='prenom' value='$prenom'>\n";
    echo "<input name='nom' value='$nom'>\n";
    for ($i = 0; $i < 3; $i++) {
        $numero = $i + 1;
        echo "<input name='note$numero' value='{$e["notes"][$i]}'>\n";
    }
    echo "<input type='submit' value='Enregistrer'>\n";
    echo "</form>\n";
}
?>
```

**Prédisez**, puis exécutez la même commande :

```bash
curl -s -d "prenom=Gabriel&nom=Moore&note1=16&note2=13&note3=14" "http://localhost/tp11/modifier.php?id=0"
```

Vous devez voir :

```text
Erreur : enregistrement impossible
```

La page signale maintenant l'échec. Rendez à votre compte le droit d'écrire dans le fichier :

```bash
chmod u+w data.json
```

Envoyez les données une dernière fois :

```bash
curl -s -d "prenom=Gabriel&nom=Moore&note1=16&note2=13&note3=14" "http://localhost/tp11/modifier.php?id=0"
```

Vous devez voir :

```text
Dossier enregistré
```

## Pour aller plus loin

- Ajoutez dans la fiche d'un étudiant un lien « Modifier » vers `modifier.php`.
- Faites afficher une page de remerciement après l'enregistrement, avec un lien de retour vers la liste.
