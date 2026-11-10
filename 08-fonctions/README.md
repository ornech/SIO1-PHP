# Écrire ses propres fonctions

À la fin de ce TP, vous saurez :

- définir une fonction et l'appeler ;
- transmettre des valeurs à une fonction avec des paramètres ;
- renvoyer un résultat avec `return` et le réutiliser ;
- expliquer pourquoi une variable créée dans une fonction n'existe pas à l'extérieur ;
- lire l'erreur « Too few arguments ».

Prérequis : les chapitres 3 à 7. Créez un dossier `tp08` et placez votre terminal dedans.

## Définir et appeler une fonction

Vous avez déjà appelé des fonctions fournies par PHP, comme `strlen()` ou `count()` : ce sont des fonctions **internes**. Une fonction que vous écrivez vous-même est une fonction **personnalisée**. Elle réunit des instructions sous un nom, pour les réutiliser sans les recopier. **Définir** une fonction, c'est l'écrire ; **appeler** une fonction, c'est l'exécuter.

Dans `tp08`, créez un fichier `fonctions.php` :

```php
<?php
function salut() {
    echo "Salut !\n";
}
salut();
salut();
?>
```

- Lignes 2 à 4 : définissent la fonction `salut`. Le mot `function`, le nom, des parenthèses vides, puis le **corps** de la fonction entre accolades. La définition n'affiche rien.
- Lignes 5 et 6 : appellent la fonction. Chaque appel exécute le corps.

**Prédisez** combien de fois `Salut !` va s'afficher, puis exécutez `php fonctions.php`.

Vous devez voir :

```text
Salut !
Salut !
```

## Transmettre des valeurs : les paramètres

**Modifiez une seule chose.** Ajoutez un paramètre à la fonction : ligne 2, écrivez `function salut($prenom) {` ; ligne 3, affichez `"Salut $prenom !\n"` ; lignes 5 et 6, appelez `salut("Léa")` puis `salut("Denis")`. Un **paramètre** est une variable écrite entre les parenthèses de la définition. La valeur donnée à l'appel, appelée **argument**, est placée dedans.

```php
<?php
function salut($prenom) {
    echo "Salut $prenom !\n";
}
salut("Léa");
salut("Denis");
?>
```

**Prédisez** les deux lignes, puis exécutez le script.

Vous devez voir :

```text
Salut Léa !
Salut Denis !
```

Une fonction peut avoir plusieurs paramètres, séparés par des virgules. Créez un fichier `additionne.php` :

```php
<?php
function additionne($a, $b) {
    $c = $a + $b;
    echo $c, "\n";
}
additionne(1, 2);
additionne(10, 5);
?>
```

- Ligne 2 : la fonction a deux paramètres, `$a` et `$b`.
- Ligne 3 : le corps calcule leur somme et la range dans `$c`.
- Lignes 6 et 7 : les deux appels donnent chacun deux arguments. Le premier argument va dans `$a`, le second dans `$b`.

**Prédisez** les deux lignes, puis exécutez `php additionne.php`.

Vous devez voir :

```text
3
15
```

## Lire l'erreur « Too few arguments »

**Modifiez une seule chose.** Remplacez les lignes 6 et 7 par un seul appel : `additionne(1);`. Ce changement ne donne qu'un argument à une fonction qui en attend deux.

```php
<?php
function additionne($a, $b) {
    $c = $a + $b;
    echo $c, "\n";
}
additionne(1);
?>
```

**Prédisez** ce que PHP va afficher, puis exécutez le script.

Vous devez voir :

```text
PHP Fatal error:  Uncaught ArgumentCountError: Too few arguments to function additionne(), 1 passed in …/tp08/additionne.php on line 6 and exactly 2 expected in …/tp08/additionne.php:2
Stack trace:
#0 …/tp08/additionne.php(6): additionne()
#1 {main}
  thrown in …/tp08/additionne.php on line 2
```

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine. Lisez le message :

- `Fatal error: Uncaught ArgumentCountError` : erreur fatale, PHP arrête le script. `ArgumentCountError` signifie que le nombre d'arguments est incorrect.
- `Too few arguments to function additionne(), 1 passed … and exactly 2 expected` : trop peu d'arguments pour la fonction `additionne()`. On en a donné 1, elle en attend exactement 2.
- `on line 6` : la ligne de l'appel, qui contient l'erreur.
- `additionne.php:2` : la ligne de la définition de la fonction.
- `Stack trace` : la liste des appels qui ont mené à l'erreur. Ici, la ligne 6 a appelé `additionne()`.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

Remettez les deux appels des lignes 6 et 7.

## Renvoyer un résultat : return

Une fonction qui affiche son résultat avec `echo` ne permet pas de le réutiliser. Avec `return`, elle renvoie le résultat à l'endroit où elle a été appelée. Créez un fichier `retour.php` :

```php
<?php
function additionne($a, $b) {
    return $a + $b;
}
$somme = additionne(5, 3);
echo $somme, "\n";
echo additionne(1, 2) * 10, "\n";
?>
```

- Ligne 3 : `return` renvoie la somme et termine la fonction.
- Ligne 5 : l'appel `additionne(5, 3)` est remplacé par la valeur renvoyée, 8, qui est rangée dans `$somme`.
- Ligne 7 : l'appel `additionne(1, 2)` est remplacé par 3, puis multiplié par 10.

**Prédisez** les deux lignes, puis exécutez `php retour.php`.

Vous devez voir :

```text
8
30
```

**Modifiez une seule chose.** Ligne 3, remplacez `return $a + $b;` par `echo $a + $b, "\n";`. Ce changement affiche la somme au lieu de la renvoyer.

```php
<?php
function additionne($a, $b) {
    echo $a + $b, "\n";
}
$somme = additionne(5, 3);
echo $somme, "\n";
echo additionne(1, 2) * 10, "\n";
?>
```

**Prédisez** les lignes affichées, puis exécutez le script.

Vous devez voir :

```text
8

3
0
```

Les valeurs `8` et `3` s'affichent pendant les appels des lignes 5 et 7, par le `echo` de la fonction. La deuxième ligne est vide : la fonction ne renvoie rien, donc `$somme` ne contient rien. Enfin, `additionne(1, 2) * 10` vaut 0, car une fonction qui ne renvoie rien donne `null`, converti en 0 dans un calcul. Remettez `return $a + $b;`.

## Variables locales

Créez un fichier `portee.php` :

```php
<?php
function exemple() {
    $local = "Je suis dans la fonction";
    echo $local, "\n";
}
exemple();
echo $local, "\n";
?>
```

**Prédisez** ce que les lignes 6 et 7 vont afficher, puis exécutez `php portee.php`.

Vous devez voir :

```text
Je suis dans la fonction
PHP Warning:  Undefined variable $local in …/tp08/portee.php on line 7

```

La variable `$local` est **locale** : elle n'existe que pendant l'exécution de la fonction. À la ligne 7, en dehors de la fonction, PHP ne la connaît pas : c'est l'avertissement `Undefined variable` du chapitre 3.

Le contraire est vrai aussi : une fonction ne voit pas les variables créées à l'extérieur. **Modifiez le fichier `portee.php`** : remplacez tout son contenu par le script suivant.

```php
<?php
$nom = "Léa";
function salut() {
    echo "Salut $nom !\n";
}
salut();
?>
```

**Prédisez** ce que PHP va afficher, puis exécutez le script.

Vous devez voir :

```text
PHP Warning:  Undefined variable $nom in …/tp08/portee.php on line 4
Salut  !
```

La variable `$nom` existe à l'extérieur de la fonction, mais pas à l'intérieur. La bonne méthode est de la transmettre en argument.

**Modifiez une seule chose.** Ligne 3, écrivez `function salut($nom) {`, et ligne 6, appelez `salut($nom);`. Ce changement ajoute un paramètre et lui donne la valeur de la variable extérieure.

```php
<?php
$nom = "Léa";
function salut($nom) {
    echo "Salut $nom !\n";
}
salut($nom);
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Salut Léa !
```

> [!NOTE]
> global et static
>
> PHP propose deux mots pour assouplir cette règle. Écrire `global $nom;` au début d'une fonction lui donne accès à la variable `$nom` créée à l'extérieur. Écrire `static $n = 0;` dans une fonction conserve la valeur de `$n` d'un appel à l'autre. Les variables globales rendent le code plus difficile à lire et à corriger : privilégiez les paramètres et `return`.

## Exercice

Créez un fichier `exercice.php` qui définit quatre fonctions, puis les appelle :

1. `doubler($n)` affiche le double de `$n`, avec `echo` ;
2. `diviser($a, $b)` renvoie le quotient de `$a` par `$b`, avec `return` ;
3. `perimetre($rayon)` renvoie le périmètre d'un cercle, soit 2 × π × rayon, avec la fonction interne `pi()` ;
4. `table_de($n)` affiche, avec une boucle `for`, les trois premières lignes de la table de multiplication de `$n`, sous la forme `3 x 1 = 3`.

Appelez-les dans cet ordre : `doubler(21)`, puis `echo diviser(10, 4)`, puis `echo perimetre(1)`, puis `table_de(3)`. Chaque résultat s'affiche suivi d'un retour à la ligne.

Exécutez `php exercice.php`. Vous devez voir :

```text
42
2.5
6.2831853071796
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
```
