# Installer PHP et écrire un premier script

À la fin de ce TP, vous saurez :

- installer PHP sous Linux ou sous Windows ;
- vérifier l'installation avec la commande `php -v` ;
- écrire un script PHP et l'exécuter avec la commande `php` ;
- expliquer le rôle des balises `<?php` et `?>` ;
- lire un message d'erreur de syntaxe : fichier, ligne, nature.

Prérequis : savoir ouvrir un terminal (Linux) ou une invite de commandes (Windows), et disposer d'un éditeur de texte brut, par exemple Visual Studio Code, Notepad++ ou nano. Un traitement de texte comme Word ne convient pas.

> [!NOTE]
> Version utilisée
>
> Les sorties de ce cours viennent de PHP 8.4.27, exécuté sous Ubuntu. Le numéro de version et certains messages peuvent différer sur votre machine.

## Installer PHP

Un **terminal** est une fenêtre dans laquelle on tape des commandes. Une **commande** est un ordre écrit, que l'on valide avec la touche Entrée.

**Sous Linux (Debian, Ubuntu).** `sudo` donne à une commande les droits d'administrateur. `apt` télécharge et installe les logiciels, appelés « paquets ».

```bash
sudo apt update
sudo apt install php
```

- `sudo apt update` met à jour la liste des paquets disponibles.
- `sudo apt install php` installe le paquet `php`.

**Sous Windows.** La variable d'environnement **PATH** est la liste des dossiers dans lesquels le système cherche les commandes que vous tapez.

1. Téléchargez la version **non-thread-safe** de PHP pour Windows : <https://windows.php.net/download/>.
2. Décompressez le fichier téléchargé dans un dossier de votre choix, par exemple `C:\PHP`.
3. Ouvrez les propriétés de votre système, puis l'onglet « Avancé », puis « Variables d'environnement ».
4. Dans « Variables système », sélectionnez la variable `PATH`, cliquez sur « Modifier » et ajoutez `;C:\PHP` à la fin.
5. Cliquez sur « OK », fermez les terminaux ouverts, puis ouvrez-en un nouveau.

## Vérifier l'installation

La commande `php -v` affiche la version de PHP (`-v` signifie « version »).

**Prédisez** ce que vous allez voir, puis exécutez :

```bash
php -v
```

Vous devez voir, sur la machine de rédaction :

```text
PHP 8.4.27 (cli) (built: Oct 21 2026 14:34:07) (NTS)
Copyright (c) The PHP Group
Built by Ubuntu
Zend Engine v4.4.27, Copyright (c) Zend Technologies
    with Zend OPcache v8.4.27, Copyright (c), by Zend Technologies
```

Comparez la première ligne avec la vôtre : `PHP 8.4.27` est le numéro de version (8 : version majeure, 4 : mineure, 27 : correctif), et `(cli)` indique que PHP s'exécute en ligne de commande. Les lignes suivantes dépendent de votre installation.

Si le terminal ne trouve pas la commande `php`, PHP n'est pas installé ou son dossier ne figure pas dans le `PATH`.

## Écrire le premier script

Créez un dossier `tp01`, puis placez votre terminal dedans :

```bash
mkdir tp01
cd tp01
```

- `mkdir tp01` crée le dossier.
- `cd tp01` change le **répertoire de travail**, c'est-à-dire le dossier dans lequel se trouve le terminal. La commande `php` y cherche les fichiers que vous lui donnez.

Ces deux commandes n'affichent rien quand elles réussissent.

Un **script** est un fichier texte qui contient des instructions pour PHP. Dans `tp01`, créez un fichier `premier.php` :

```php
<?php
echo "Bonjour";
?>
```

- Ligne 1 : `<?php` ouvre le code PHP.
- Ligne 2 : `echo` est une **instruction** qui affiche du texte. `"Bonjour"` est une **chaîne de caractères** : un texte écrit entre guillemets droits. Le point-virgule `;` termine l'instruction.
- Ligne 3 : `?>` ferme le code PHP.

**Prédisez** ce que le programme va afficher, et sur combien de lignes, puis exécutez le script :

```bash
php premier.php
```

Vous devez voir :

```text
Bonjour
```

PHP n'ajoute pas de retour à la ligne après le texte : l'invite du terminal peut s'afficher juste à la suite de `Bonjour`.

## À quoi servent `<?php` et `?>`

PHP affiche tel quel ce qui se trouve en dehors des balises, et exécute ce qui se trouve entre `<?php` et `?>`. Vérifiez-le : créez un fichier `balises.php` qui contient du texte avant et après le code.

```php
Avant
<?php echo "milieu"; ?>
Après
```

**Prédisez** ce qui va s'afficher, puis exécutez `php balises.php`.

Vous devez voir :

```text
Avant
milieuAprès
```

- `Avant` et `Après` sont en dehors des balises : PHP les affiche sans les modifier.
- `milieu` vient de l'instruction placée entre `<?php` et `?>`.
- `milieu` et `Après` sont sur la même ligne : PHP n'affiche pas le retour à la ligne placé juste après `?>`.

## Afficher plusieurs textes

Revenez au fichier `premier.php`.

**Modifiez une seule chose.** Ajoutez une ligne 3 : `echo "tout le monde";`. Cette ligne demande à PHP d'afficher un second texte.

```php
<?php
echo "Bonjour";
echo "tout le monde";
?>
```

**Prédisez** : y a-t-il un espace entre `Bonjour` et `tout` ? Exécutez le script.

Vous devez voir :

```text
Bonjourtout le monde
```

`echo` n'ajoute ni espace ni retour à la ligne : il affiche seulement ce qui se trouve entre les guillemets.

**Modifiez une seule chose.** Ligne 2, ajoutez un espace avant le guillemet fermant : `"Bonjour "` au lieu de `"Bonjour"`. Ce changement ajoute un espace au texte affiché.

```php
<?php
echo "Bonjour ";
echo "tout le monde";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Bonjour tout le monde
```

**Modifiez une seule chose.** Ligne 2, remplacez l'espace avant le guillemet fermant par `\n` : `"Bonjour\n"`. Dans une chaîne entre guillemets doubles, `\n` représente un retour à la ligne. Ce changement supprime l'espace et ajoute un retour à la ligne après `Bonjour`.

```php
<?php
echo "Bonjour\n";
echo "tout le monde";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Bonjour
tout le monde
```

## Lire une erreur de syntaxe

**Modifiez une seule chose.** Ligne 2, supprimez le point-virgule à la fin de l'instruction : `echo "Bonjour\n"` au lieu de `echo "Bonjour\n";`. Ce changement supprime la fin de l'instruction.

```php
<?php
echo "Bonjour\n"
echo "tout le monde";
?>
```

**Prédisez** : le script va-t-il afficher `Bonjour` avant de s'arrêter ? Exécutez-le.

Vous devez voir :

```text
PHP Parse error:  syntax error, unexpected token "echo", expecting "," or ";" in …/tp01/premier.php on line 3
```

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine. Lisez le message :

- `PHP Parse error` : erreur d'analyse du code. PHP lit tout le fichier avant de l'exécuter. Il refuse ce fichier, donc aucun texte n'est affiché.
- `syntax error, unexpected token "echo"` : erreur de syntaxe. PHP rencontre un `echo` là où il ne l'attendait pas.
- `expecting "," or ";"` : à cet endroit, PHP attendait une virgule ou un point-virgule.
- `in …/tp01/premier.php` : le fichier concerné.
- `on line 3` : la ligne où PHP s'est arrêté. C'est la ligne qui suit l'oubli : PHP ne voit le point-virgule manquant qu'en lisant le `echo` suivant.

> [!WARNING]
> Message d'erreur
>
> Le texte d'un message d'erreur dépend de la version de PHP et de sa configuration (`php.ini`). Ces messages viennent de PHP 8.4.27. Sur votre machine, le message peut s'afficher sans le préfixe `PHP`, ou deux fois.

Remettez le point-virgule à la fin de la ligne 2.

## Écrire un commentaire

Un **commentaire** est un texte écrit pour les humains, que PHP ignore. Il commence par `//` et s'arrête à la fin de la ligne. Pour plusieurs lignes, on l'écrit entre `/*` et `*/`.

**Modifiez une seule chose.** Ajoutez une ligne 2 : `// Mon premier script`. Cette ligne est un commentaire : elle n'ajoute rien à ce que PHP exécute.

```php
<?php
// Mon premier script
echo "Bonjour\n";
echo "tout le monde";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Bonjour
tout le monde
```

**Modifiez une seule chose.** Ligne 4, ajoutez `// ` au début de l'instruction : `// echo "tout le monde";`. Ce changement transforme l'instruction en commentaire : PHP ne l'exécute plus.

```php
<?php
// Mon premier script
echo "Bonjour\n";
// echo "tout le monde";
?>
```

**Prédisez**, puis exécutez le script.

Vous devez voir :

```text
Bonjour
```

## Exercice

Créez un fichier `identite.php` qui affiche exactement ces deux lignes, chacune terminée par un retour à la ligne :

```text
Nom : Dupont
Prénom : Léa
```

Exécutez `php identite.php` et comparez avec le texte ci-dessus.
