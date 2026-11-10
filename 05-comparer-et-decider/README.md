# Comparer et décider

À la fin de ce TP, vous saurez :

- comparer deux valeurs avec `==`, `===`, `!=`, `<`, `>`, `<=` et `>=` ;
- écrire une décision avec `if`, `elseif` et `else` ;
- combiner des conditions avec `&&`, `||` et `!` ;
- choisir entre plusieurs cas avec `switch`, ou en une ligne avec `?:` ;
- lire l'erreur « Unclosed '{' ».

Prérequis : les chapitres 2 et 3. Créez un dossier `tp05` et placez votre terminal dedans.

## Comparer deux valeurs

Une **condition** est une question dont la réponse est vraie ou fausse : un booléen, comme au chapitre 2. On la pose avec un **opérateur de comparaison**.

| Opérateur | Nom | La condition est vraie si… |
| --- | --- | --- |
| `==` | égal | les deux valeurs sont égales |
| `===` | identique | les deux valeurs sont égales et de même type |
| `!=` ou `<>` | différent | les deux valeurs ne sont pas égales |
| `!==` | non identique | les valeurs sont différentes ou de types différents |
| `>` | plus grand que | la valeur de gauche est supérieure à celle de droite |
| `<` | plus petit que | la valeur de gauche est inférieure à celle de droite |
| `>=` | plus grand ou égal | la valeur de gauche est supérieure ou égale |
| `<=` | plus petit ou égal | la valeur de gauche est inférieure ou égale |

Dans `tp05`, créez un fichier `comparaisons.php` :

```php
<?php
$a = 10;
$b = 2;
var_dump($a > $b);
var_dump($a == $b);
var_dump($a != $b);
?>
```

**Prédisez** les trois lignes, puis exécutez `php comparaisons.php`.

Vous devez voir :

```text
bool(true)
bool(false)
bool(true)
```

**Modifiez le fichier `comparaisons.php`** : remplacez tout son contenu par le script suivant, qui compare des valeurs de types différents.

```php
<?php
var_dump(5 == "5");
var_dump(5 === "5");
var_dump("10" == "1e1");
var_dump(null == false);
?>
```

**Prédisez** les quatre lignes, puis exécutez le script.

Vous devez voir :

```text
bool(true)
bool(false)
bool(true)
bool(true)
```

L'opérateur `==` convertit les valeurs avant de les comparer : le nombre `5` et le texte `"5"` sont égaux, et `"10"` et `"1e1"` aussi (1e1 s'écrit 1 × 10¹, soit 10). L'opérateur `===` compare aussi le type : `5` et `"5"` ne sont pas identiques. Quand les types des deux valeurs peuvent différer, utilisez `===`.

## Décider avec if, elseif et else

Créez un fichier `decision.php`. L'instruction `if` exécute un bloc de code seulement si la condition est vraie. Le bloc est délimité par des accolades `{` et `}` :

```php
<?php
$a = 10;
$b = 2;
if ($a > $b) {
    echo "a est plus grand que b\n";
}
?>
```

- Ligne 4 : `if ($a > $b) {` pose la condition entre parenthèses et ouvre le bloc.
- Ligne 5 : n'est exécutée que si la condition est vraie. Le retrait de 4 espaces rend le bloc lisible.
- Ligne 6 : `}` ferme le bloc.

**Prédisez** ce que le script va afficher, puis exécutez `php decision.php`.

Vous devez voir :

```text
a est plus grand que b
```

**Modifiez une seule chose.** Ligne 2, remplacez `10` par `1`. Ce changement rend la condition fausse.

```php
<?php
$a = 1;
$b = 2;
if ($a > $b) {
    echo "a est plus grand que b\n";
}
?>
```

**Prédisez** ce que le script va afficher, puis exécutez-le. Vous ne devez rien voir : la condition est fausse, et PHP ignore le bloc.

**Modifiez une seule chose.** Ligne 6, remplacez `}` par `} else {`, puis ajoutez deux lignes : l'affichage du `else` et une ligne `}`. Le bloc `else` s'exécute quand la condition du `if` est fausse.

```php
<?php
$a = 1;
$b = 2;
if ($a > $b) {
    echo "a est plus grand que b\n";
} else {
    echo "a n'est pas plus grand que b\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
a n'est pas plus grand que b
```

Le texte du `else` dit « n'est pas plus grand » et non « est plus petit » : le `else` couvre aussi le cas où `$a` et `$b` sont égaux. Pour distinguer trois cas, on ajoute un `elseif`, qui pose une seconde condition.

**Modifiez une seule chose.** Lignes 6 à 8, remplacez le bloc `else` par un `elseif ($a < $b)` qui affiche `a est plus petit que b`, suivi d'un nouveau `else` qui affiche `a est égal à b`.

```php
<?php
$a = 1;
$b = 2;
if ($a > $b) {
    echo "a est plus grand que b\n";
} elseif ($a < $b) {
    echo "a est plus petit que b\n";
} else {
    echo "a est égal à b\n";
}
?>
```

PHP teste les conditions dans l'ordre et exécute le premier bloc dont la condition est vraie. Si aucune ne l'est, il exécute le `else`.

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
a est plus petit que b
```

**Modifiez une seule chose.** Ligne 2, remplacez `1` par `2`. Ce changement rend `$a` égal à `$b`.

```php
<?php
$a = 2;
$b = 2;
if ($a > $b) {
    echo "a est plus grand que b\n";
} elseif ($a < $b) {
    echo "a est plus petit que b\n";
} else {
    echo "a est égal à b\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
a est égal à b
```

## Lire l'erreur « Unclosed '{' »

**Modifiez une seule chose.** Ligne 2, remettez `1`, puis supprimez la ligne `}` qui ferme le bloc `else` (la ligne 10). Ce changement laisse une accolade ouverte sans accolade fermante.

```php
<?php
$a = 1;
$b = 2;
if ($a > $b) {
    echo "a est plus grand que b\n";
} elseif ($a < $b) {
    echo "a est plus petit que b\n";
} else {
    echo "a est égal à b\n";
?>
```

**Prédisez** ce que PHP va afficher, puis exécutez le script.

Vous devez voir :

```text
PHP Parse error:  Unclosed '{' on line 8 in …/tp05/decision.php on line 11
```

Lisez le message :

- `Parse error` : erreur d'analyse, comme au chapitre 1. Aucun texte n'est affiché.
- `Unclosed '{' on line 8` : l'accolade ouvrante de la ligne 8 (`} else {`) n'est jamais fermée.
- `in …/tp05/decision.php on line 11` : PHP a atteint la fin du fichier à la ligne 11 sans trouver la fermeture. Le fichier se termine par un retour à la ligne : sans lui, PHP indiquerait la ligne 10.

Remettez la ligne `}` avant `?>`.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

## Combiner des conditions

Trois opérateurs combinent des conditions : `&&` (et : les deux conditions sont vraies), `||` (ou : au moins une est vraie) et `!` (non : inverse la condition). Créez un fichier `combiner.php` :

```php
<?php
$age = 20;
$jour = "samedi";
if ($age >= 18 && $age < 65) {
    echo "Âge de travail\n";
}
if ($jour == "samedi" || $jour == "dimanche") {
    echo "Week-end\n";
}
if (!($age >= 18)) {
    echo "Mineur\n";
}
?>
```

**Prédisez** les lignes affichées, puis exécutez `php combiner.php`.

Vous devez voir :

```text
Âge de travail
Week-end
```

**Modifiez une seule chose.** Ligne 2, remplacez `20` par `15`.

```php
<?php
$age = 15;
$jour = "samedi";
if ($age >= 18 && $age < 65) {
    echo "Âge de travail\n";
}
if ($jour == "samedi" || $jour == "dimanche") {
    echo "Week-end\n";
}
if (!($age >= 18)) {
    echo "Mineur\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Week-end
Mineur
```

> [!NOTE]
> and et or
>
> PHP accepte aussi les mots `and` et `or`, mais ils s'appliquent après l'affectation : avec `$a = true and false;`, la variable `$a` vaut `true`. Utilisez `&&` et `||`.

## Choisir avec switch

L'instruction `switch` compare une valeur à plusieurs cas. Créez un fichier `couleur.php` :

```php
<?php
$couleur = "vert";
switch ($couleur) {
    case "rouge":
        echo "Bonjour\n";
        break;
    case "vert":
        echo "Bienvenue\n";
        break;
    default:
        echo "Les goûts et les couleurs, ça ne se discute pas\n";
}
?>
```

- Ligne 3 : `switch ($couleur)` indique la valeur à comparer.
- Lignes 4 et 7 : chaque `case` est un cas. PHP exécute le bloc du premier cas dont la valeur est égale (au sens de `==`).
- Lignes 6 et 9 : `break` quitte le `switch`.
- Ligne 10 : `default` est le cas par défaut, utilisé quand aucun `case` ne correspond.

**Prédisez** ce que le script va afficher, puis exécutez `php couleur.php`.

Vous devez voir :

```text
Bienvenue
```

**Modifiez une seule chose.** Ligne 2, remplacez `"vert"` par `"bleu"`.

```php
<?php
$couleur = "bleu";
switch ($couleur) {
    case "rouge":
        echo "Bonjour\n";
        break;
    case "vert":
        echo "Bienvenue\n";
        break;
    default:
        echo "Les goûts et les couleurs, ça ne se discute pas\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Les goûts et les couleurs, ça ne se discute pas
```

**Modifiez une seule chose.** Remettez `"vert"` à la ligne 2, puis supprimez la ligne 9 (`break;` du cas `"vert"`). Ce changement retire l'instruction qui quitte le `switch`.

```php
<?php
$couleur = "vert";
switch ($couleur) {
    case "rouge":
        echo "Bonjour\n";
        break;
    case "vert":
        echo "Bienvenue\n";
    default:
        echo "Les goûts et les couleurs, ça ne se discute pas\n";
}
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Bienvenue
Les goûts et les couleurs, ça ne se discute pas
```

Sans `break`, PHP ne quitte pas le `switch` : il continue d'exécuter les instructions du cas suivant, même si ce cas ne correspond pas. Remettez le `break;`.

## Décider en une ligne

L'opérateur `?:` choisit entre deux valeurs selon une condition. Il s'écrit `condition ? valeur_si_vraie : valeur_si_fausse`. Créez un fichier `mention.php` :

```php
<?php
$note = 12;
$mention = $note >= 10 ? "admis" : "refusé";
echo $mention, "\n";
?>
```

**Prédisez** la mention affichée, puis exécutez `php mention.php`.

Vous devez voir :

```text
admis
```

## Exercice

Créez un fichier `exercice.php`. Au début, créez les variables `$a` (valeur 7), `$b` (valeur 5) et `$couleur` (valeur `"rouge"`). Affichez ensuite, une par ligne, les quatre réponses suivantes :

1. `Bonjour tout le monde`, si `$a` est supérieur à `$b` ;
2. `oui` si `$a` est égal à `$b`, sinon `non` ;
3. `1` si `$a` est égal à `$b`, `2` si `$a` est supérieur à `$b`, sinon `3` ;
4. avec un `switch` sur `$couleur` : `Bonjour` si elle vaut `"rouge"`, `bienvenue` si elle vaut `"vert"`, sinon `Les goûts et mes couleurs, ça ne se discute pas`.

Exécutez `php exercice.php`. Vous devez voir :

```text
Bonjour tout le monde
non
2
Bonjour
```
