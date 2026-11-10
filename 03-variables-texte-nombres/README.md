# Les variables : texte et nombres

À la fin de ce TP, vous saurez :

- créer une variable et afficher sa valeur avec `echo` ;
- assembler du texte et des variables ;
- reconnaître le type d'une valeur (texte, entier, décimal, booléen) avec `var_dump()` ;
- appliquer des fonctions à un texte : `strlen()`, `strrev()`, `str_replace()`, `strpos()` ;
- lire un avertissement « variable non définie ».

Prérequis : le chapitre 1 (écrire et exécuter un script). Créez un dossier `tp03` et placez votre terminal dedans.

## Créer une variable

Une **variable** est comme un carton de déménagement. On écrit un nom dessus, puis on met quelque chose dedans : une donnée. Ce que l'on met dans le carton s'appelle sa **valeur**.

En PHP, on crée une variable en écrivant `$`, un nom, le signe `=` et la valeur. Le signe `=` est l'**opérateur d'affectation** : il place la valeur de droite dans la variable de gauche.

Dans `tp03`, créez un fichier `variables.php` :

```php
<?php
$nom = "Denis";
echo $nom;
?>
```

- Ligne 2 : crée la variable `$nom` et y place la chaîne `"Denis"`.
- Ligne 3 : `echo $nom;` affiche le contenu de la variable, pas le mot `$nom`.

**Prédisez** ce que le script va afficher, puis exécutez `php variables.php`.

Vous devez voir :

```text
Denis
```

Une variable est conservée dans la mémoire de l'ordinateur (la RAM), pas sur le disque : elle disparaît quand le script se termine. Pour conserver une donnée, il faut l'enregistrer ailleurs, par exemple dans un fichier ou une base de données.

> [!NOTE]
> Nom d'une variable
>
> Un nom peut contenir des chiffres, mais pas au début : `$nomPersonne8` est valide, alors que `$8nom` provoque une erreur de syntaxe (`unexpected integer "8"`).

## Lire un avertissement

**Modifiez une seule chose.** Ligne 3, remplacez `$nom` par `$Nom` (avec un `N` majuscule). Ce changement désigne une variable que le script n'a jamais créée.

```php
<?php
$nom = "Denis";
echo $Nom;
?>
```

**Prédisez** : le script va-t-il afficher `Denis` ? Exécutez-le.

Vous devez voir :

```text
PHP Warning:  Undefined variable $Nom in …/tp03/variables.php on line 3
```

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine. Lisez le message :

- `Warning` : avertissement. Contrairement à l'erreur de syntaxe du chapitre 1, PHP a lu le fichier sans le refuser : il signale le problème à la ligne 3, pendant l'exécution.
- `Undefined variable $Nom` : la variable `$Nom` n'existe pas.
- `in …/tp03/variables.php on line 3` : le fichier et la ligne concernés.

PHP distingue les majuscules des minuscules dans les noms de variables : `$nom` et `$Nom` sont deux variables différentes. Remettez `$nom` à la ligne 3.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27.

## Assembler du texte et des variables

**Modifiez une seule chose.** Ligne 3, remplacez `echo $nom;` par `echo "Nom : ", $nom, "\n";`. La commande `echo` accepte plusieurs valeurs séparées par des virgules et les affiche l'une après l'autre.

```php
<?php
$nom = "Denis";
echo "Nom : ", $nom, "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Nom : Denis
```

**Modifiez une seule chose.** Ajoutez une variable `$prenom` et son affichage : une ligne 3 `$prenom = "Roger";` et une ligne 5 `echo "Prénom : ", $prenom, "\n";`.

```php
<?php
$nom = "Denis";
$prenom = "Roger";
echo "Nom : ", $nom, "\n";
echo "Prénom : ", $prenom, "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Nom : Denis
Prénom : Roger
```

**Modifiez une seule chose.** Lignes 4 et 5, remplacez chaque virgule par un point. L'opérateur **point** (`.`) colle deux textes pour n'en faire qu'un : c'est la **concaténation**.

```php
<?php
$nom = "Denis";
$prenom = "Roger";
echo "Nom : " . $nom . "\n";
echo "Prénom : " . $prenom . "\n";
?>
```

**Prédisez** : l'affichage change-t-il ? Exécutez le script.

Vous devez voir :

```text
Nom : Denis
Prénom : Roger
```

L'affichage est le même : la virgule fait afficher plusieurs valeurs, le point fabrique un seul texte.

**Modifiez une seule chose.** Lignes 4 et 5, supprimez les points et écrivez la variable directement dans le texte : `echo "Nom : $nom\n";`. Dans un texte entre guillemets doubles, PHP remplace `$nom` par sa valeur.

```php
<?php
$nom = "Denis";
$prenom = "Roger";
echo "Nom : $nom\n";
echo "Prénom : $prenom\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Nom : Denis
Prénom : Roger
```

**Modifiez une seule chose.** Ligne 4, remplacez les guillemets doubles par des guillemets simples : `echo 'Nom : $nom\n';`.

```php
<?php
$nom = "Denis";
$prenom = "Roger";
echo 'Nom : $nom\n';
echo "Prénom : $prenom\n";
?>
```

**Prédisez** ce que la ligne 4 va afficher, puis exécutez le script.

Vous devez voir :

```text
Nom : $nom\nPrénom : Roger
```

Entre guillemets simples, PHP n'interprète rien : `$nom` et `\n` s'affichent tels quels, et le retour à la ligne n'a pas lieu.

## Les types de valeurs

Une valeur a un **type** : sa nature. Ce chapitre en utilise quatre.

| Type | Exemple | Signification |
| --- | --- | --- |
| chaîne de caractères (`string`) | `"Denis"` | un texte |
| entier (`int`) | `268` | un nombre sans virgule |
| décimal (`float`) | `61.875` | un nombre à virgule, écrite avec un point |
| booléen (`bool`) | `true` | vrai (`true`) ou faux (`false`) |

La fonction `var_dump()` affiche le type d'une valeur et la valeur elle-même. Créez un fichier `types.php` :

```php
<?php
$texte = "Denis";
$entier = 268;
$decimal = 61.875;
$vrai = true;
var_dump($texte);
var_dump($entier);
var_dump($decimal);
var_dump($vrai);
?>
```

**Prédisez** ce que chaque `var_dump()` va afficher, puis exécutez `php types.php`.

Vous devez voir :

```text
string(5) "Denis"
int(268)
float(61.875)
bool(true)
```

`string(5)` signifie « texte de 5 caractères ». PHP utilise le point, et non la virgule, pour les nombres décimaux.

Le type change le résultat. **Modifiez le fichier `types.php`** : remplacez tout son contenu par :

```php
<?php
echo "3" . "5", "\n";
echo 3 + 5, "\n";
?>
```

**Prédisez** les deux lignes, puis exécutez le script.

Vous devez voir :

```text
35
8
```

Le point colle les deux textes `"3"` et `"5"`. L'opérateur `+` additionne les deux nombres `3` et `5`. Les opérateurs de calcul sont détaillés dans le chapitre suivant.

> [!NOTE]
> Texte et addition
>
> Avec l'opérateur `+`, PHP convertit un texte qui ressemble à un nombre : `"3" + "5"` donne le nombre `8`, pas le texte `35`.

## Appliquer des fonctions à un texte

Une **fonction** est une opération déjà écrite, que l'on appelle par son nom en lui donnant des valeurs entre parenthèses, appelées **arguments**. Elle renvoie un résultat que `echo` peut afficher. Créez un fichier `chaines.php` :

```php
<?php
$phrase = "Hello world!";
echo strlen($phrase), "\n";
echo strrev("Salut!"), "\n";
echo str_replace("a", "b", "abc abc abc"), "\n";
?>
```

- Ligne 3 : `strlen()` renvoie la longueur du texte, en nombre de caractères.
- Ligne 4 : `strrev()` renvoie le texte à l'envers.
- Ligne 5 : `str_replace()` remplace chaque `a` par un `b` dans le texte `"abc abc abc"`. Ses trois arguments sont : le texte cherché, son remplaçant, le texte d'origine.

**Prédisez** les trois lignes, puis exécutez `php chaines.php`.

Vous devez voir :

```text
12
!tulaS
bbc bbc bbc
```

Créez maintenant un fichier `position.php`. La fonction `strpos()` renvoie la position de la première occurrence d'un texte dans un autre.

```php
<?php
$phrase = "Hello world!";
echo strpos($phrase, "world"), "\n";
?>
```

**Prédisez** la position de `world`, puis exécutez `php position.php`.

Vous devez voir :

```text
6
```

Les positions se comptent à partir de 0 : `H` est à la position 0, et `Hello ` occupe les positions 0 à 5, donc `world` commence à la position 6.

**Modifiez une seule chose.** Ligne 3, remplacez `"world"` par `"Hello"`. Ce changement cherche un texte situé au tout début de la phrase.

```php
<?php
$phrase = "Hello world!";
echo strpos($phrase, "Hello"), "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
0
```

**Modifiez une seule chose.** Ligne 3, remplacez `"Hello"` par `"Bonjour"`. Ce changement cherche un texte qui n'est pas dans la phrase.

```php
<?php
$phrase = "Hello world!";
echo strpos($phrase, "Bonjour"), "\n";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir une ligne vide :

```text

```

**Modifiez une seule chose.** Ajoutez une ligne 4 : `var_dump(strpos($phrase, "Bonjour"));`. Cette ligne affiche le type et la valeur renvoyés par `strpos()`.

```php
<?php
$phrase = "Hello world!";
echo strpos($phrase, "Bonjour"), "\n";
var_dump(strpos($phrase, "Bonjour"));
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text

bool(false)
```

Quand le texte n'est pas trouvé, `strpos()` renvoie le booléen `false`. La commande `echo` affiche `false` comme un texte vide : c'est pourquoi la première ligne est vide.

## Exercice

Créez un fichier `fiche.php` avec quatre variables `$nom`, `$prenom`, `$adresse` et `$email`, dont les valeurs sont `Dupont`, `Léa`, `12 rue des Lilas` et `lea.dupont@example.org`. Affichez-les exactement ainsi, une ligne par variable :

```text
Nom : Dupont
Prénom : Léa
Adresse : 12 rue des Lilas
Email : lea.dupont@example.org
```

Exécutez `php fiche.php` et comparez avec le texte ci-dessus.
