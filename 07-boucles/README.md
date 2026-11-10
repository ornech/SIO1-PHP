# Répéter avec les boucles

À la fin de ce TP, vous saurez :

- répéter des instructions avec les boucles `while`, `do … while` et `for` ;
- dire à quel moment chaque boucle teste sa condition ;
- compter avec une boucle `for` et choisir son pas ;
- parcourir un tableau avec `foreach`, avec ou sans clé ;
- lire les avertissements d'un `foreach` appliqué à une variable absente.

Prérequis : les TP 4, 5 et 6. Créez un dossier `tp07` et placez votre terminal dedans.

## Répéter tant qu'une condition est vraie : while

Une **boucle** répète un bloc d'instructions. Chaque répétition s'appelle une **itération**. La boucle `while` (« tant que ») répète son bloc tant que sa condition est vraie.

Dans `tp07`, créez un fichier `boucle.php` :

```php
<?php
$x = 1;
while ($x < 5) {
    echo "x vaut $x\n";
    $x++;
}
?>
```

- Ligne 2 : `$x` vaut 1 au départ.
- Ligne 3 : `while ($x < 5) {` teste la condition avant chaque itération. Tant qu'elle est vraie, PHP exécute le bloc.
- Ligne 4 : affiche la valeur de `$x`.
- Ligne 5 : `$x++` ajoute 1 à `$x` (TP 4). Sans cette ligne, la condition resterait vraie pour toujours.

**Prédisez** combien de lignes le script va afficher, et lesquelles, puis exécutez `php boucle.php`.

Vous devez voir :

```text
x vaut 1
x vaut 2
x vaut 3
x vaut 4
```

PHP teste `$x < 5` avant chaque itération. Quand `$x` vaut 5, la condition est fausse : la boucle s'arrête, et `x vaut 5` n'est jamais affiché.

> [!WARNING]
> Boucle infinie
>
> Si la condition ne devient jamais fausse, par exemple parce que vous avez supprimé la ligne `$x++`, la boucle ne s'arrête jamais. Appuyez sur Ctrl+C dans le terminal pour interrompre le programme.

**Modifiez une seule chose.** Ligne 2, remplacez `1` par `10`. Ce changement rend la condition fausse dès le premier test.

```php
<?php
$x = 10;
while ($x < 5) {
    echo "x vaut $x\n";
    $x++;
}
?>
```

**Prédisez** ce que le script va afficher, puis exécutez-le. Vous ne devez rien voir : la condition est fausse avant la première itération, donc le bloc n'est jamais exécuté.

## Tester la condition à la fin : do … while

**Modifiez une seule chose.** Remplacez la ligne `while ($x < 5) {` par `do {`, et la ligne `}` par `} while ($x < 5);`. La condition est maintenant testée à la fin de chaque itération.

```php
<?php
$x = 10;
do {
    echo "x vaut $x\n";
    $x++;
} while ($x < 5);
?>
```

**Prédisez** : la condition est fausse dès le départ, le texte va-t-il s'afficher ? Exécutez le script.

Vous devez voir :

```text
x vaut 10
```

Avec `do … while`, le bloc s'exécute toujours au moins une fois, puisque la condition n'est testée qu'après la première itération. Avec `while`, il peut ne jamais s'exécuter.

## Compter avec for

La boucle `for` regroupe sur une seule ligne les trois éléments d'un compteur : `for (départ; condition; pas)`. Créez un fichier `compter.php` :

```php
<?php
for ($i = 1; $i <= 5; $i++) {
    echo "Tour $i\n";
}
?>
```

- `$i = 1` s'exécute une seule fois, avant la première itération.
- `$i <= 5` est testé avant chaque itération, comme dans un `while`.
- `$i++` s'exécute à la fin de chaque itération.

**Prédisez** les lignes affichées, puis exécutez `php compter.php`.

Vous devez voir :

```text
Tour 1
Tour 2
Tour 3
Tour 4
Tour 5
```

**Modifiez une seule chose.** Ligne 3, remplacez l'instruction `echo "Tour $i\n";` par `echo "3 x $i = ", 3 * $i, "\n";`. Cette ligne affiche une ligne de la table de multiplication de 3.

```php
<?php
for ($i = 1; $i <= 5; $i++) {
    echo "3 x $i = ", 3 * $i, "\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
3 x 4 = 12
3 x 5 = 15
```

**Modifiez une seule chose.** Remettez `echo "Tour $i\n";` à la ligne 3, puis ligne 2, remplacez `$i++` par `$i += 2`. Ce changement fait avancer le compteur de 2 à chaque itération.

```php
<?php
for ($i = 1; $i <= 5; $i += 2) {
    echo "Tour $i\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Tour 1
Tour 3
Tour 5
```

## Parcourir un tableau : foreach

La boucle `foreach` (« pour chaque ») fait une itération par élément d'un tableau, sans compteur. Créez un fichier `parcourir.php` :

```php
<?php
$couleurs = ["rouge", "vert", "bleu", "jaune"];
foreach ($couleurs as $valeur) {
    echo "La valeur est $valeur\n";
}
?>
```

Ligne 3 : `foreach ($couleurs as $valeur) {` se lit « pour chaque élément de `$couleurs`, placer sa valeur dans `$valeur` et exécuter le bloc ».

**Prédisez** les lignes affichées, puis exécutez `php parcourir.php`.

Vous devez voir :

```text
La valeur est rouge
La valeur est vert
La valeur est bleu
La valeur est jaune
```

Pour un tableau associatif, `foreach` peut aussi fournir la clé : on écrit `$cle => $valeur`, comme dans la création du tableau. Créez un fichier `cles.php` :

```php
<?php
$age = ["Peter" => 35, "Ben" => 37, "Joe" => 43];
foreach ($age as $cle => $valeur) {
    echo "La clé est $cle pour la valeur $valeur\n";
}
?>
```

**Prédisez** les lignes affichées, puis exécutez `php cles.php`.

Vous devez voir :

```text
La clé est Peter pour la valeur 35
La clé est Ben pour la valeur 37
La clé est Joe pour la valeur 43
```

## Lire les avertissements d'un foreach

Revenez au fichier `parcourir.php`.

**Modifiez une seule chose.** Ligne 3, remplacez `$couleurs` par `$couleur` (sans `s`). Ce changement désigne une variable qui n'existe pas.

```php
<?php
$couleurs = ["rouge", "vert", "bleu", "jaune"];
foreach ($couleur as $valeur) {
    echo "La valeur est $valeur\n";
}
?>
```

**Prédisez** ce que PHP va afficher, puis exécutez le script.

Vous devez voir :

```text
PHP Warning:  Undefined variable $couleur in …/tp07/parcourir.php on line 3
PHP Warning:  foreach() argument must be of type array|object, null given in …/tp07/parcourir.php on line 3
```

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine. Lisez les deux messages, qui portent sur la même ligne 3 :

- `Undefined variable $couleur` : la variable `$couleur` n'existe pas, comme au TP 3. C'est la cause.
- `foreach() argument must be of type array|object, null given` : `foreach` attend un tableau (ou un objet), et reçoit `null`, la valeur d'une variable qui n'existe pas. C'est la conséquence : le bloc n'est pas exécuté.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

Remettez `$couleurs` à la ligne 3.

## Exercice

Créez un fichier `exercice.php` qui affiche, dans cet ordre :

1. avec une boucle `while` : les nombres 20, 15, 10 et 5, un par ligne, en partant de 20 et en retirant 5 à chaque itération tant que le nombre est supérieur à 0 ;
2. avec une boucle `for` : les trois premières lignes de la table de multiplication de 4, sous la forme `4 x 1 = 4` ;
3. avec un `foreach` sur le tableau associatif `["janvier" => 31, "février" => 28, "mars" => 31]` : une ligne par mois, sous la forme `Le mois de janvier contient 31 jours` ;
4. avec un `foreach` sur le tableau associatif `["Mercure" => "57 909 050", "Vénus" => "108 208 475"]` : une ligne par planète, sous la forme `Mercure est à 57 909 050 km du Soleil`.

Exécutez `php exercice.php`. Vous devez voir :

```text
20
15
10
5
4 x 1 = 4
4 x 2 = 8
4 x 3 = 12
Le mois de janvier contient 31 jours
Le mois de février contient 28 jours
Le mois de mars contient 31 jours
Mercure est à 57 909 050 km du Soleil
Vénus est à 108 208 475 km du Soleil
```
