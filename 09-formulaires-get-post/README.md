# Les formulaires : envoyer des données avec GET et POST

À la fin de ce TP, vous saurez :

- envoyer des données dans une URL (méthode GET) et les lire avec `$_GET` ;
- écrire un formulaire HTML avec les attributs `action`, `method` et `name` ;
- envoyer des données avec la méthode POST et les lire avec `$_POST` ;
- afficher une saisie sans risque avec `htmlspecialchars()` ;
- lire l'avertissement « Undefined array key » et le corriger avec `??`.

Prérequis : les chapitres 4, 6 et 8, et un serveur Apache avec PHP. Créez un dossier `tp09` dans la racine du serveur (`/var/www/html` sous Linux) : tous les fichiers de ce chapitre y sont enregistrés.

## Envoyer des données dans l'URL

Une URL peut transporter des données. Après le chemin, un point d'interrogation `?` introduit des paires `clé=valeur`, séparées par `&`. On parle de requête **GET**. Par exemple, dans `http://localhost/tp09/get.php?nom=Doe&prenom=John` :

- `?` commence la série de paires ;
- `nom=Doe` est une paire : la clé `nom` a la valeur `Doe` ;
- `&` sépare les paires ;
- `prenom=John` est la seconde paire.

Côté PHP, la **super-globale** `$_GET` contient ces paires. Une super-globale est une variable prédéfinie, toujours disponible. `$_GET` est un tableau associatif (chapitre 4) : les clés sont les noms, les valeurs sont celles de l'URL.

Dans `tp09`, créez un fichier `get.php` :

```php
<?php
echo $_GET["nom"], "\n";
?>
```

La ligne 2 affiche la valeur associée à la clé `nom`. Envoyez une requête avec deux paires. Les guillemets autour de l'URL sont nécessaires, car le caractère `&` a un sens particulier pour le terminal :

```bash
curl "http://localhost/tp09/get.php?nom=Doe&prenom=John"
```

**Prédisez** ce que le serveur va répondre, puis exécutez la commande.

Vous devez voir :

```text
Doe
```

**Modifiez le fichier `get.php`** : remplacez tout son contenu par le script suivant, qui affiche toutes les paires reçues avec une boucle `foreach` (chapitre 6).

```php
<?php
foreach ($_GET as $cle => $valeur) {
    echo "$cle : $valeur\n";
}
?>
```

**Prédisez** les lignes affichées, puis exécutez la commande :

```bash
curl "http://localhost/tp09/get.php?variable=test&nom=Doe&prenom=John"
```

Vous devez voir :

```text
variable : test
nom : Doe
prenom : John
```

**Modifiez une seule chose.** Dans l'URL, remplacez `Doe` par `Jean+Paul` et supprimez les autres paires. Le caractère `+` représente un espace dans une valeur.

```bash
curl "http://localhost/tp09/get.php?nom=Jean+Paul"
```

**Prédisez** la ligne affichée, puis exécutez la commande.

Vous devez voir :

```text
nom : Jean Paul
```

## Lire un avertissement : la clé absente

Créez un fichier `salut.php` :

```php
<?php
echo "Bonjour [", $_GET["nom"], "]\n";
?>
```

**Prédisez** la réponse du serveur quand l'URL ne contient aucune paire, puis exécutez la commande :

```bash
curl http://localhost/tp09/salut.php
```

Vous devez voir :

```text
Bonjour []
```

Aucun message d'erreur n'apparaît dans la page : la configuration de PHP envoie les avertissements dans le journal d'erreurs d'Apache. Cherchez-y le dernier avertissement :

```bash
sudo grep -o "PHP Warning:.*" /var/log/apache2/error.log | tail -1
```

Vous devez voir :

```text
PHP Warning:  Undefined array key "nom" in /var/www/html/tp09/salut.php on line 2
```

Lisez le message :

- `Warning` : avertissement, comme aux chapitres précédents.
- `Undefined array key "nom"` : la clé `"nom"` n'existe pas dans le tableau. L'URL n'envoyait pas de paire `nom=…`.
- `in /var/www/html/tp09/salut.php on line 2` : le fichier et la ligne concernés.

> [!WARNING]
> Journal et configuration
>
> L'emplacement du journal (`/var/log/apache2/error.log` sous Debian et Ubuntu) et l'affichage des messages dépendent du système et de la configuration de PHP (`php.ini`). Ces messages viennent de PHP 8.4.27.

**Modifiez une seule chose.** Ligne 2, remplacez `$_GET["nom"]` par `$_GET["nom"] ?? "inconnu"`. L'opérateur `??` fournit la valeur de droite quand la clé de gauche n'existe pas.

```php
<?php
echo "Bonjour [", $_GET["nom"] ?? "inconnu", "]\n";
?>
```

**Prédisez** la réponse sans paire, puis avec `?nom=Lea`. Exécutez les deux commandes :

```bash
curl http://localhost/tp09/salut.php
```

Vous devez voir :

```text
Bonjour [inconnu]
```

```bash
curl "http://localhost/tp09/salut.php?nom=Lea"
```

Vous devez voir :

```text
Bonjour [Lea]
```

## Le formulaire HTML

Un navigateur fabrique l'URL à votre place quand l'utilisateur remplit un **formulaire** HTML. Dans `tp09`, créez un fichier `get.html` :

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
<form action="/tp09/get.php" method="GET">
    <input type="text" name="nom">
    <input type="submit" value="Envoyer">
</form>
</body>
</html>
```

Une balise HTML peut contenir des **attributs**, écrits dans la balise ouvrante sous la forme `nom="valeur"`.

- `<meta charset="UTF-8">` : indique le jeu de caractères, pour que les accents s'affichent correctement.
- `<form action="/tp09/get.php" method="GET">` : l'attribut `action` donne la page qui reçoit les données, l'attribut `method` donne la méthode d'envoi.
- `<input type="text" name="nom">` : un champ de saisie de texte. L'attribut `name` est le nom de la clé envoyée : sans lui, le champ n'est pas transmis.
- `<input type="submit" value="Envoyer">` : le bouton qui envoie le formulaire. L'attribut `value` est le texte du bouton.

**Prédisez** l'URL qui s'affichera dans la barre d'adresse après l'envoi, puis ouvrez `http://localhost/tp09/get.html` dans un navigateur, saisissez `Lea` et cliquez sur « Envoyer ».

Le navigateur envoie la même requête que cette commande, et la page affiche le même résultat :

```bash
curl "http://localhost/tp09/get.php?nom=Lea"
```

Vous devez voir :

```text
nom : Lea
```

L'URL de la barre d'adresse est donc `http://localhost/tp09/get.php?nom=Lea`.

## Envoyer des données avec POST

Avec la méthode **POST**, les données ne sont pas dans l'URL : le navigateur les place dans le corps de la requête. PHP les met à disposition dans la super-globale `$_POST`, un tableau associatif comme `$_GET`.

Créez un fichier `post.php` qui contient à la fois le formulaire et le code PHP qui lit ses données :

```php
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
<form action="post.php" method="POST">
    <label for="nom">Nom :</label>
    <input type="text" id="nom" name="nom">
    <input type="submit" value="Envoyer">
</form>
<?php
$nom = $_POST["nom"] ?? "";
echo "Nom reçu : <b>$nom</b>\n";
?>
</body>
</html>
```

- Ligne 7 : `method="POST"` choisit la méthode POST, et `action="post.php"` renvoie les données à la page elle-même.
- Ligne 13 : lit la clé `nom` de `$_POST`, avec `""` si elle n'existe pas (par exemple quand la page est ouverte sans avoir envoyé le formulaire).
- Ligne 14 : affiche la valeur reçue en gras.

La commande suivante affiche la ligne qui contient `Nom reçu`, sans que rien n'ait été envoyé :

```bash
curl -s http://localhost/tp09/post.php | grep "Nom reçu"
```

**Prédisez** la ligne affichée, puis exécutez la commande.

Vous devez voir :

```text
Nom reçu : <b></b>
```

**Modifiez une seule chose.** Ajoutez l'option `-d "nom=Dupont"` à la commande. L'option `-d` envoie les données dans le corps d'une requête POST, comme le fait un formulaire.

```bash
curl -s -d "nom=Dupont" http://localhost/tp09/post.php | grep "Nom reçu"
```

**Prédisez**, puis exécutez la commande.

Vous devez voir :

```text
Nom reçu : <b>Dupont</b>
```

**Modifiez une seule chose.** Envoyez la valeur dans l'URL, avec une requête GET : retirez l'option `-d` et ajoutez `?nom=Dupont` à l'URL.

```bash
curl -s "http://localhost/tp09/post.php?nom=Dupont" | grep "Nom reçu"
```

**Prédisez** : `$_POST` va-t-il lire la valeur placée dans l'URL ? Exécutez la commande.

Vous devez voir :

```text
Nom reçu : <b></b>
```

`$_POST` ne contient que les données du corps d'une requête POST, et `$_GET` que celles de l'URL.

## Ne jamais afficher une saisie telle quelle

La valeur de `$nom` vient de l'utilisateur : il peut y écrire n'importe quel texte, y compris des balises HTML. **Prédisez** ce que le serveur va renvoyer quand la saisie est `<i>Dupont</i>` :

```bash
curl -s -d "nom=<i>Dupont</i>" http://localhost/tp09/post.php | grep "Nom reçu"
```

Vous devez voir :

```text
Nom reçu : <b><i>Dupont</i></b>
```

La saisie est insérée telle quelle dans la page : le navigateur la traiterait comme du HTML, et pas comme du texte.

**Modifiez une seule chose.** Dans le fichier `post.php`, ligne 14, remplacez `$nom` par `" . htmlspecialchars($nom) . "`. La fonction `htmlspecialchars()` remplace les caractères `<`, `>`, `&` et `"` par des codes (`&lt;`, `&gt;`, `&amp;`, `&quot;`) que le navigateur affiche comme du texte.

```php
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
<form action="post.php" method="POST">
    <label for="nom">Nom :</label>
    <input type="text" id="nom" name="nom">
    <input type="submit" value="Envoyer">
</form>
<?php
$nom = $_POST["nom"] ?? "";
echo "Nom reçu : <b>" . htmlspecialchars($nom) . "</b>\n";
?>
</body>
</html>
```

**Prédisez**, puis exécutez la même commande :

```bash
curl -s -d "nom=<i>Dupont</i>" http://localhost/tp09/post.php | grep "Nom reçu"
```

Vous devez voir :

```text
Nom reçu : <b>&lt;i&gt;Dupont&lt;/i&gt;</b>
```

Le navigateur affiche maintenant `<i>Dupont</i>` comme un texte. Appliquez `htmlspecialchars()` à toute donnée venue de l'utilisateur avant de l'écrire dans une page.

## GET ou POST ?

| | GET | POST |
| --- | --- | --- |
| Où sont les données ? | dans l'URL, après `?` | dans le corps de la requête |
| Variable PHP | `$_GET` | `$_POST` |
| Visibles dans l'URL | oui | non |
| Conservées dans l'historique et les favoris | oui | non |
| Usage typique | demander une page, lancer une recherche | envoyer un formulaire |

N'envoyez jamais de donnée sensible, comme un mot de passe, avec GET : elle apparaît dans l'URL.

## Exercice

Créez un fichier `livre.html` qui contient un formulaire GET vers `/tp09/livre.php`, avec quatre champs de noms `auteur`, `livre`, `isbn` et `editeur`. Créez un fichier `livre.php` qui lit ces quatre valeurs avec `$_GET` et `htmlspecialchars()`, et qui affiche une ligne par valeur.

Envoyez les données `Frank Herbert`, `Dune`, `2266320548` et `POCKET` :

```bash
curl "http://localhost/tp09/livre.php?auteur=Frank+Herbert&livre=Dune&isbn=2266320548&editeur=POCKET"
```

Vous devez voir :

```text
Auteur : Frank Herbert
Livre : Dune
ISBN : 2266320548
Éditeur : POCKET
```
