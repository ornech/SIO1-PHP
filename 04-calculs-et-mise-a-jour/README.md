# Calculer et mettre à jour une variable

À la fin de ce TP, vous saurez :

- calculer avec les opérateurs `+`, `-`, `*`, `/`, `%` et `**` ;
- prévoir le type du résultat d'une division et appliquer la priorité des opérations ;
- mettre à jour une variable avec `+=`, `-=`, `*=`, `/=` et `%=` ;
- ajouter ou retirer 1 avec `++` et `--` ;
- lire l'erreur « division par zéro ».

Prérequis : le chapitre 3 (variables, `echo`, `var_dump()`). Créez un dossier `tp04` et placez votre terminal dedans.

## Les opérateurs de calcul

Un **opérateur** est un symbole qui combine des valeurs, appelées **opérandes**, pour produire un résultat. Dans `100 + 13`, `+` est l'opérateur, `100` et `13` sont les opérandes.

| Opérateur | Nom | Ce qu'il calcule |
| --- | --- | --- |
| `+` | addition | la somme des deux opérandes |
| `-` | soustraction | la différence |
| `*` | multiplication | le produit |
| `/` | division | le quotient |
| `%` | modulo | le reste de la division entière |
| `**` | puissance | le premier opérande élevé à la puissance du second |

Dans `tp04`, créez un fichier `calculs.php` :

```php
<?php
$x = 100;
$y = 13;
echo $x + $y, "\n";
echo $x - $y, "\n";
echo $x * $y, "\n";
?>
```

- Lignes 2 et 3 : créent les variables `$x` et `$y`.
- Lignes 4 à 6 : affichent la somme, la différence et le produit de `$x` et `$y`, chacun suivi d'un retour à la ligne.

**Prédisez** les trois lignes, puis exécutez `php calculs.php`.

Vous devez voir :

```text
113
87
1300
```

**Modifiez une seule chose.** Ajoutez une ligne 7 : `echo $x / $y, "\n";`. Cette ligne affiche le quotient de 100 par 13.

```php
<?php
$x = 100;
$y = 13;
echo $x + $y, "\n";
echo $x - $y, "\n";
echo $x * $y, "\n";
echo $x / $y, "\n";
?>
```

**Prédisez** la quatrième ligne, puis exécutez le script.

Vous devez voir :

```text
113
87
1300
7.6923076923077
```

PHP affiche 14 chiffres significatifs au maximum.

**Modifiez une seule chose.** Ajoutez une ligne 8 : `echo $x % $y, "\n";`. Le modulo est le reste de la division entière : 100 = 13 × 7 + 9, donc le reste est 9.

```php
<?php
$x = 100;
$y = 13;
echo $x + $y, "\n";
echo $x - $y, "\n";
echo $x * $y, "\n";
echo $x / $y, "\n";
echo $x % $y, "\n";
?>
```

**Prédisez** la cinquième ligne, puis exécutez le script.

Vous devez voir :

```text
113
87
1300
7.6923076923077
9
```

**Modifiez une seule chose.** Ajoutez une ligne 9 : `echo $y ** 2, "\n";`. Cette ligne élève 13 à la puissance 2, c'est-à-dire 13 × 13.

```php
<?php
$x = 100;
$y = 13;
echo $x + $y, "\n";
echo $x - $y, "\n";
echo $x * $y, "\n";
echo $x / $y, "\n";
echo $x % $y, "\n";
echo $y ** 2, "\n";
?>
```

**Prédisez** la sixième ligne, puis exécutez le script.

Vous devez voir :

```text
113
87
1300
7.6923076923077
9
169
```

## Le type et la priorité

Créez un fichier `quotient.php` :

```php
<?php
var_dump(6 / 3);
var_dump(7 / 2);
?>
```

**Prédisez** le type de chaque résultat (`int` ou `float`), puis exécutez `php quotient.php`.

Vous devez voir :

```text
int(2)
float(3.5)
```

La division renvoie un entier quand le résultat est un nombre entier, et un décimal sinon.

Créez un fichier `priorite.php` :

```php
<?php
echo 2 + 3 * 4, "\n";
echo (2 + 3) * 4, "\n";
?>
```

**Prédisez** les deux lignes, puis exécutez `php priorite.php`.

Vous devez voir :

```text
14
20
```

PHP effectue la multiplication et la division avant l'addition et la soustraction : dans la ligne 2, `3 * 4` est calculé en premier. Les parenthèses passent avant : dans la ligne 3, `2 + 3` est calculé en premier.

## Lire une erreur de division

Créez un fichier `division.php` :

```php
<?php
$a = 10;
$b = 0;
echo $a / $b, "\n";
?>
```

**Prédisez** ce que PHP va afficher, puis exécutez `php division.php`.

Vous devez voir :

```text
PHP Fatal error:  Uncaught DivisionByZeroError: Division by zero in …/tp04/division.php:4
Stack trace:
#0 {main}
  thrown in …/tp04/division.php on line 4
```

Lisez le message :

- `Fatal error` : erreur fatale. PHP arrête le script.
- `Uncaught DivisionByZeroError: Division by zero` : la nature de l'erreur. « Division by zero » signifie « division par zéro ». « Uncaught » signifie que le script ne prévoit rien pour traiter cette erreur.
- `in …/tp04/division.php:4` : le fichier, puis la ligne (après les deux-points) où l'erreur s'est produite.
- `Stack trace: #0 {main}` : le chemin parcouru pour arriver à l'erreur. Ici, l'erreur se trouve directement dans le script principal (`{main}`).

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

## Mettre à jour une variable

Créez un fichier `miseajour.php` :

```php
<?php
$x = 100;
$y = 13;
$x = $x + $y;
echo $x, "\n";
?>
```

La ligne 4 se lit de droite à gauche : PHP calcule `$x + $y`, puis range le résultat dans `$x`. C'est comme ouvrir le carton `$x`, y ajouter 13 et le refermer.

**Prédisez** la valeur affichée, puis exécutez `php miseajour.php`.

Vous devez voir :

```text
113
```

**Modifiez une seule chose.** Ligne 4, remplacez `$x = $x + $y;` par `$x += $y;`. Le raccourci `+=` ajoute le second opérande à la variable.

```php
<?php
$x = 100;
$y = 13;
$x += $y;
echo $x, "\n";
?>
```

**Prédisez** : l'affichage change-t-il ? Exécutez le script.

Vous devez voir :

```text
113
```

**Modifiez une seule chose.** Ligne 4, remplacez `+=` par `*=`. Le raccourci `*=` multiplie la variable par le second opérande.

```php
<?php
$x = 100;
$y = 13;
$x *= $y;
echo $x, "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
1300
```

Chaque opérateur de calcul a son raccourci :

| Raccourci | Équivalent à |
| --- | --- |
| `$x += $y` | `$x = $x + $y` |
| `$x -= $y` | `$x = $x - $y` |
| `$x *= $y` | `$x = $x * $y` |
| `$x /= $y` | `$x = $x / $y` |
| `$x %= $y` | `$x = $x % $y` |

## Ajouter ou retirer 1

Ajouter 1 à une variable est si fréquent que PHP a un raccourci : `$x++` ajoute 1, `$x--` retire 1. Créez un fichier `compteur.php` :

```php
<?php
$x = 5;
$x++;
echo $x, "\n";
$x--;
$x--;
echo $x, "\n";
?>
```

**Prédisez** les deux lignes, puis exécutez `php compteur.php`.

Vous devez voir :

```text
6
4
```

Créez un fichier `avant-apres.php` pour voir si la position de `++` compte :

```php
<?php
$x = 5;
echo $x++, "\n";
echo $x, "\n";
?>
```

**Prédisez** les deux lignes, puis exécutez le script.

Vous devez voir :

```text
5
6
```

Écrit après la variable, `$x++` fournit d'abord la valeur actuelle (5), puis ajoute 1.

**Modifiez une seule chose.** Ligne 3, déplacez `++` avant la variable : `echo ++$x, "\n";`.

```php
<?php
$x = 5;
echo ++$x, "\n";
echo $x, "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
6
6
```

Écrit avant la variable, `++$x` ajoute d'abord 1, puis fournit la nouvelle valeur (6).

## Exercice

Créez un fichier `exercice.php` qui affiche quatre valeurs, une par ligne, calculées par PHP :

1. le reste de la division de 8 par 5 ;
2. la valeur qui suit 377 dans la suite de Fibonacci, où chaque valeur est la somme des deux précédentes (0, 1, 1, 2, 3, 5, 8, …, 144, 233, 377) ;
3. la valeur correspondant à 27 quand 33 correspond à 53 (règle de trois) ;
4. le résultat de 8 augmenté de 5, en utilisant `+=`.

Exécutez `php exercice.php`. Vous devez voir :

```text
3
610
43.363636363636
13
```
