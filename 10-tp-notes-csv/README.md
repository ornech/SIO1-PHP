# TP : les notes des étudiants (fichier CSV)

À la fin de ce TP, vous saurez :

- lire un fichier CSV dans un tableau PHP avec `file()` et `str_getcsv()` ;
- parcourir un tableau de tableaux et calculer la moyenne de la classe pour chaque épreuve ;
- produire un tableau HTML avec une boucle ;
- afficher la fiche d'un étudiant choisi par un paramètre d'URL ;
- lire l'erreur d'un fichier introuvable.

Prérequis : les chapitres 4 à 9. Créez un dossier `tp10` dans la racine du serveur (`/var/www/html` sous Linux) et placez votre terminal dedans.

Le responsable de la formation veut plus de lisibilité sur les notes de 20 étudiants, qui ont passé trois épreuves écrites notées sur 20. Les notes sont enregistrées dans un fichier CSV.

## Le fichier de données

Un fichier **CSV** (*Comma-Separated Values*) est un fichier texte où chaque ligne est un enregistrement et où les champs sont séparés par des virgules. Ici, chaque ligne contient le prénom, le nom, puis les notes des trois épreuves.

Dans `tp10`, créez un fichier `data.csv` :

```text
"Gabriel","Moore",16,13,14
"Léo","Bidelspach",20,1,8
"Raphaël","Jones",12,14,15
"Louis","Billingham",8,5,10
"Arthur","Mitchell",11,12,7
"Jules","Sutherland",14,15,10
"Maël","Simpson",14,12,14
"Noah","Afify",9,13,18
"Adam","Maloles",5,0,7
"Lucas","Munro",11,15,12
"Jade","Wright",14,5,9
"Louise","Protich",8,15,13
"Emma","Watson",11,12,1
"Ambre","Sinclair",12,7,16
"Alice","Anderson",12,15,13
"Rose","Munro",13,12,10
"Anna","Banasiewicz",11,15,13
"Alba","Donaldson",11,12,9
"Romy","Henris",14,12,18
"Mia","Hinsen",10,8,9
```

## Lire le fichier dans un tableau

Créez un fichier `lecture.php` :

```php
<?php
$data = array_map('str_getcsv', file('data.csv'));
echo count($data), "\n";
print_r($data[0]);
?>
```

- `file('data.csv')` lit le fichier et renvoie un tableau qui contient une ligne du fichier par élément.
- `str_getcsv()` découpe une ligne CSV en champs et renvoie un tableau.
- `array_map('str_getcsv', …)` appelle `str_getcsv()` sur chaque élément du tableau et renvoie le tableau des résultats : `$data` est donc un tableau de tableaux.
- `print_r()` affiche le contenu d'un tableau, de façon plus compacte que `var_dump()`.

**Prédisez** le nombre d'éléments de `$data`, puis le contenu de `$data[0]`. Exécutez `php lecture.php`.

Vous devez voir :

```text
20
Array
(
    [0] => Gabriel
    [1] => Moore
    [2] => 16
    [3] => 13
    [4] => 14
)
```

## Lire l'erreur d'un fichier introuvable

**Modifiez une seule chose.** Renommez le fichier `data.csv` en `data2.csv`. Ce changement fait disparaître le fichier que `lecture.php` cherche.

**Prédisez** ce que PHP va afficher, puis exécutez `php lecture.php`.

Vous devez voir :

```text
PHP Warning:  file(data.csv): Failed to open stream: No such file or directory in …/tp10/lecture.php on line 2
PHP Fatal error:  Uncaught TypeError: array_map(): Argument #2 ($array) must be of type array, false given in …/tp10/lecture.php:2
Stack trace:
#0 …/tp10/lecture.php(2): array_map()
#1 {main}
  thrown in …/tp10/lecture.php on line 2
```

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine. Lisez les deux messages, qui portent sur la ligne 2 :

- `Warning: file(data.csv): Failed to open stream: No such file or directory` : la cause. PHP n'a pas pu ouvrir `data.csv` : le fichier n'existe pas dans le répertoire de travail.
- `Fatal error: Uncaught TypeError: array_map(): Argument #2 ($array) must be of type array, false given` : la conséquence. Comme `file()` a échoué, il renvoie `false`, et `array_map()` attend un tableau.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

Remettez le nom `data.csv`.

## Afficher la liste des étudiants

Pour chaque étudiant, la page affiche sur une seule ligne son nom, son prénom, et pour chaque épreuve sa note puis la moyenne de la classe. Un **tableau HTML** s'écrit avec les balises `<table>` (le tableau), `<tr>` (une ligne), `<th>` (une cellule d'en-tête) et `<td>` (une cellule).

Créez un fichier `liste.php` :

```php
<?php
$data = array_map('str_getcsv', file('data.csv'));
$moyennes = [0, 0, 0];
foreach ($data as $etudiant) {
    for ($i = 0; $i < 3; $i++) {
        $moyennes[$i] += $etudiant[2 + $i];
    }
}
foreach ($moyennes as $i => $total) {
    $moyennes[$i] = round($total / count($data), 2);
}
echo "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n</head>\n<body>\n";
echo "<table border='1'>\n";
echo "<tr><th>Nom</th><th>Prénom</th><th>Épreuve 1</th><th>Moyenne 1</th><th>Épreuve 2</th><th>Moyenne 2</th><th>Épreuve 3</th><th>Moyenne 3</th></tr>\n";
foreach ($data as $numero => $etudiant) {
    echo "<tr><td><a href='etudiant.php?id=$numero'>$etudiant[1]</a></td><td>$etudiant[0]</td>";
    for ($i = 0; $i < 3; $i++) {
        echo "<td>", $etudiant[2 + $i], "</td><td>", $moyennes[$i], "</td>";
    }
    echo "</tr>\n";
}
echo "</table>\n</body>\n</html>\n";
?>
```

- Lignes 3 à 8 : `$moyennes` accumule, pour chacune des trois épreuves, la somme des notes de tous les étudiants. La note de l'épreuve `$i` se trouve à l'index `2 + $i` de la ligne de l'étudiant.
- Lignes 9 à 11 : divisent chaque somme par le nombre d'étudiants et arrondissent à deux décimales avec `round()`.
- Lignes 12 à 14 : écrivent le début de la page et la ligne d'en-tête du tableau.
- Lignes 15 à 21 : écrivent une ligne du tableau par étudiant. Le nom est un lien vers `etudiant.php`, avec l'index de l'étudiant dans l'URL.

**Prédisez** le nombre de lignes `<tr>` de la page : un en-tête et combien de lignes d'étudiants ? Exécutez la commande suivante :

```bash
curl -s http://localhost/tp10/liste.php | grep -c "<tr>"
```

Vous devez voir :

```text
21
```

**Prédisez** la moyenne de la classe à l'épreuve 1 (les notes ont des valeurs de 5 à 20), puis affichez les lignes 7 à 10 de la page :

```bash
curl -s http://localhost/tp10/liste.php | sed -n "7,10p"
```

Vous devez voir :

```text
<table border='1'>
<tr><th>Nom</th><th>Prénom</th><th>Épreuve 1</th><th>Moyenne 1</th><th>Épreuve 2</th><th>Moyenne 2</th><th>Épreuve 3</th><th>Moyenne 3</th></tr>
<tr><td><a href='etudiant.php?id=0'>Moore</a></td><td>Gabriel</td><td>16</td><td>11.8</td><td>13</td><td>10.65</td><td>14</td><td>11.3</td></tr>
<tr><td><a href='etudiant.php?id=1'>Bidelspach</a></td><td>Léo</td><td>20</td><td>11.8</td><td>1</td><td>10.65</td><td>8</td><td>11.3</td></tr>
```

Ouvrez `http://localhost/tp10/liste.php` dans un navigateur : la page affiche un tableau de 21 lignes. Les moyennes de la classe sont 11.8, 10.65 et 11.3.

## Afficher la fiche d'un étudiant

Créez un fichier `etudiant.php`, vers lequel pointent les liens de la liste :

```php
<?php
$data = array_map('str_getcsv', file('data.csv'));
$id = $_GET["id"] ?? "";
if (!isset($data[$id])) {
    echo "Étudiant introuvable\n";
} else {
    $e = $data[$id];
    echo "<h1>", htmlspecialchars($e[1]), " ", htmlspecialchars($e[0]), "</h1>\n";
    echo "<ul>\n";
    for ($i = 0; $i < 3; $i++) {
        echo "<li>Épreuve ", $i + 1, " : ", $e[2 + $i], "</li>\n";
    }
    echo "</ul>\n";
}
?>
```

- Ligne 3 : lit le paramètre `id` de l'URL, avec une chaîne vide s'il est absent (chapitre 9).
- Ligne 4 : `isset($data[$id])` vaut `true` si le tableau contient une entrée à cet index. Le `!` inverse le résultat : le bloc `if` s'exécute quand l'étudiant n'existe pas.
- Lignes 7 à 13 : affichent le nom, le prénom et les trois notes de l'étudiant choisi.

**Prédisez** la réponse pour `?id=1`, puis exécutez la commande :

```bash
curl -s "http://localhost/tp10/etudiant.php?id=1"
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

**Modifiez une seule chose.** Remplacez `id=1` par `id=99`. Il n'y a pas d'étudiant à l'index 99.

```bash
curl -s "http://localhost/tp10/etudiant.php?id=99"
```

**Prédisez**, puis exécutez la commande.

Vous devez voir :

```text
Étudiant introuvable
```

Le même message s'affiche quand l'URL ne contient pas de paramètre `id`.

## Pour aller plus loin

- Ajoutez dans la liste une colonne « Rang » qui donne le classement de chaque étudiant, selon la somme de ses trois notes.
- Améliorez la présentation de la liste et des fiches avec une feuille de style CSS.
