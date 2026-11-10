# Les tableaux

À la fin de ce TP, vous saurez :

- créer un tableau indexé et un tableau associatif ;
- lire, modifier et ajouter une valeur avec son index ou sa clé ;
- compter les éléments d'un tableau et les trier ;
- réunir et comparer deux tableaux avec `+`, `==` et `===` ;
- lire l'avertissement « Array to string conversion ».

Prérequis : les TP 3 et 4. Créez un dossier `tp05` et placez votre terminal dedans.

## Qu'est-ce qu'un tableau ?

Un **tableau** (en anglais *array*) est une variable qui contient plusieurs valeurs. Si une variable est un carton de déménagement, un tableau est une étagère de cartons. Chaque carton de l'étagère s'appelle un **élément**.

- Dans un tableau **indexé**, on retrouve un élément grâce à son **index**, un numéro. Le premier élément a l'index 0.
- Dans un tableau **associatif**, on retrouve un élément grâce à sa **clé**, un nom que vous choisissez. Chaque clé est associée à une valeur.

## Créer un tableau indexé

Dans `tp05`, créez un fichier `fruits.php` :

```php
<?php
$fruits = ["pomme", "cerise", "banane"];
var_dump($fruits);
?>
```

- Ligne 2 : crée le tableau `$fruits`. Les valeurs sont écrites entre crochets, séparées par des virgules.
- Ligne 3 : `var_dump()` affiche le contenu du tableau.

**Prédisez** l'index de `"cerise"`, puis exécutez `php fruits.php`.

Vous devez voir :

```text
array(3) {
  [0]=>
  string(5) "pomme"
  [1]=>
  string(6) "cerise"
  [2]=>
  string(6) "banane"
}
```

`array(3)` indique un tableau de 3 éléments. Chaque élément est précédé de son index entre crochets, puis du type et de la valeur, comme au TP 3.

> [!NOTE]
> Autre écriture
>
> Vous trouverez aussi `array("pomme", "cerise", "banane")` à la place des crochets. Le résultat est identique.

## Lire, modifier et ajouter un élément

L'**interpréteur interactif** de PHP permet d'essayer une instruction sans créer de fichier. Lancez-le avec la commande `php -a`. PHP affiche l'invite `php >` et attend une instruction. Tapez ensuite `$fruits = ["pomme", "cerise", "banane"];`, puis `echo $fruits[2];`.

**Prédisez** la valeur affichée : `pomme` ou `banane` ?

Vous devez voir :

```text
Interactive shell

php > $fruits = ["pomme", "cerise", "banane"];
php > echo $fruits[2];
banane
```

L'index 2 désigne le troisième élément, car la numérotation commence à 0.

**Modifiez une seule chose.** Tapez `$fruits[1] = "kiwi";`, puis `echo $fruits[1];`. La première instruction remplace la valeur de l'index 1.

**Prédisez** la valeur affichée.

Vous devez voir :

```text
php > $fruits[1] = "kiwi";
php > echo $fruits[1];
kiwi
```

**Modifiez une seule chose.** Tapez `$fruits[] = "fraise";`, puis `echo count($fruits);`. Des crochets vides ajoutent un élément à la fin du tableau. La fonction `count()` renvoie le nombre d'éléments.

**Prédisez** le nombre affiché.

Vous devez voir :

```text
php > $fruits[] = "fraise";
php > echo count($fruits);
4
```

## Lire un avertissement

Un élément d'un tableau peut être lui-même un tableau : c'est un **tableau imbriqué**. Dans la même session, tapez `$t = [9999, [0, 1, 2]];`, puis `echo $t[1];`. L'élément d'index 1 est le tableau `[0, 1, 2]`.

**Prédisez** ce que `echo` va afficher.

Vous devez voir :

```text
php > $t = [9999, [0, 1, 2]];
php > echo $t[1];
PHP Warning:  Array to string conversion in php shell code on line 1
Array
```

Lisez le message :

- `Warning` : avertissement. PHP continue de fonctionner.
- `Array to string conversion` : conversion d'un tableau en texte. La commande `echo` affiche du texte, et PHP ne sait pas transformer un tableau en texte : il écrit seulement le mot `Array`.
- `in php shell code on line 1` : la ligne 1 de ce que vous venez de taper. Il n'y a pas de fichier.

**Modifiez une seule chose.** Tapez `echo $t[1][0];`. Deux index se suivent : le premier désigne le tableau imbriqué, le second désigne un élément de ce tableau. Tapez ensuite `exit` pour quitter.

**Prédisez** la valeur affichée.

Vous devez voir :

```text
php > echo $t[1][0];
0
php > exit
```

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

## Créer un tableau associatif

Créez un fichier `ages.php`. Chaque entrée s'écrit `clé => valeur` :

```php
<?php
$age = ["Denis" => 35, "Pierre" => 37, "Marie" => 24];
var_dump($age);
?>
```

**Prédisez** ce que `var_dump()` va afficher à la place des numéros d'index, puis exécutez `php ages.php`.

Vous devez voir :

```text
array(3) {
  ["Denis"]=>
  int(35)
  ["Pierre"]=>
  int(37)
  ["Marie"]=>
  int(24)
}
```

**Modifiez une seule chose.** Ligne 3, remplacez `var_dump($age);` par `echo "Denis a " . $age["Denis"] . " ans.\n";`. Pour lire une valeur, on écrit le nom du tableau suivi de la clé entre crochets.

```php
<?php
$age = ["Denis" => 35, "Pierre" => 37, "Marie" => 24];
echo "Denis a " . $age["Denis"] . " ans.\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Denis a 35 ans.
```

**Modifiez une seule chose.** Ajoutez deux lignes à la fin, avant `?>` : `$age["Denis"] = 36;`, puis la même ligne `echo` qu'à la ligne 3. Écrire une valeur avec une clé qui existe déjà remplace l'ancienne valeur.

```php
<?php
$age = ["Denis" => 35, "Pierre" => 37, "Marie" => 24];
echo "Denis a " . $age["Denis"] . " ans.\n";
$age["Denis"] = 36;
echo "Denis a " . $age["Denis"] . " ans.\n";
?>
```

**Prédisez** les deux lignes, puis exécutez le script.

Vous devez voir :

```text
Denis a 35 ans.
Denis a 36 ans.
```

**Modifiez une seule chose.** Ajoutez deux lignes à la fin, avant `?>` : `$age["Paul"] = 19;`, puis `echo count($age), "\n";`. Écrire une valeur avec une clé qui n'existe pas encore ajoute un élément.

```php
<?php
$age = ["Denis" => 35, "Pierre" => 37, "Marie" => 24];
echo "Denis a " . $age["Denis"] . " ans.\n";
$age["Denis"] = 36;
echo "Denis a " . $age["Denis"] . " ans.\n";
$age["Paul"] = 19;
echo count($age), "\n";
?>
```

**Prédisez** les trois lignes, puis exécutez le script.

Vous devez voir :

```text
Denis a 35 ans.
Denis a 36 ans.
4
```

> [!NOTE]
> Clés convertibles
>
> Une clé doit être un entier ou un texte. PHP convertit les autres types : la clé `true` devient `1` et la clé décimale `8.15` devient `8`. Si deux clés deviennent identiques, la seconde valeur remplace la première.

## Compter et trier

Les fonctions `sort()` et `rsort()` trient un tableau indexé en ordre croissant et décroissant. La fonction `implode()` assemble les valeurs d'un tableau en un seul texte, séparées par le texte donné en premier argument. Créez un fichier `tris.php` :

```php
<?php
$nombres = [7, 38, 2, 22, 72];
sort($nombres);
echo implode(", ", $nombres), "\n";
rsort($nombres);
echo implode(", ", $nombres), "\n";
?>
```

**Prédisez** les deux lignes, puis exécutez `php tris.php`.

Vous devez voir :

```text
2, 7, 22, 38, 72
72, 38, 22, 7, 2
```

Pour un tableau associatif, la fonction `asort()` trie selon les valeurs et conserve la clé de chaque valeur. Créez un fichier `classement.php` :

```php
<?php
$age = ["Peter" => 35, "Ben" => 43, "Joe" => 37];
asort($age);
var_dump($age);
?>
```

**Prédisez** l'ordre des clés, puis exécutez `php classement.php`.

Vous devez voir :

```text
array(3) {
  ["Peter"]=>
  int(35)
  ["Joe"]=>
  int(37)
  ["Ben"]=>
  int(43)
}
```

**Modifiez une seule chose.** Ligne 3, remplacez `asort($age);` par `ksort($age);`. La fonction `ksort()` trie selon les clés, par ordre alphabétique.

```php
<?php
$age = ["Peter" => 35, "Ben" => 43, "Joe" => 37];
ksort($age);
var_dump($age);
?>
```

**Prédisez** l'ordre des clés, puis exécutez le script.

Vous devez voir :

```text
array(3) {
  ["Ben"]=>
  int(43)
  ["Joe"]=>
  int(37)
  ["Peter"]=>
  int(35)
}
```

Les fonctions `arsort()` et `krsort()` font la même chose que `asort()` et `ksort()`, dans l'ordre décroissant.

## Réunir et comparer deux tableaux

Créez un fichier `reunir.php`. L'opérateur `+` réunit deux tableaux :

```php
<?php
$x = ["a" => 1, "b" => 2];
$y = ["b" => 9, "c" => 3];
var_dump($x + $y);
?>
```

**Prédisez** : quelle valeur aura la clé `"b"`, 2 ou 9 ? Exécutez `php reunir.php`.

Vous devez voir :

```text
array(3) {
  ["a"]=>
  int(1)
  ["b"]=>
  int(2)
  ["c"]=>
  int(3)
}
```

Le résultat garde toutes les entrées du premier tableau, puis ajoute celles du second dont la clé est nouvelle.

Créez un fichier `comparer.php`. L'opérateur `==` vérifie que deux tableaux contiennent les mêmes paires clé-valeur. L'opérateur `===` vérifie en plus qu'elles sont dans le même ordre :

```php
<?php
$x = ["x" => 1, "y" => 2];
$y = ["y" => 2, "x" => 1];
var_dump($x == $y);
var_dump($x === $y);
?>
```

**Prédisez** les deux lignes, puis exécutez `php comparer.php`.

Vous devez voir :

```text
bool(true)
bool(false)
```

## Exercice

Créez un fichier `exercice.php` qui affiche trois lignes :

1. un tableau `$suite` contenant 0, 1, 1, 2, 3, 5, 8 et 13, trié par ordre décroissant, affiché avec `implode()` ;
2. un tableau associatif `$jours` qui contient janvier (31), février (28) et mars (31), puis la phrase `février : 28 jours`, avec le nombre lu dans le tableau ;
3. un tableau `$contacts` qui contient deux tableaux imbriqués, `["Denis", "Roger", "Denis.roger@serveur.io"]` et `["Fred", "Pasteur", "Fred.pasteur@serveur.io"]`, puis l'adresse e-mail de Denis Roger, lue dans le tableau.

Exécutez `php exercice.php`. Vous devez voir :

```text
13, 8, 5, 3, 2, 1, 1, 0
février : 28 jours
Denis.roger@serveur.io
```
