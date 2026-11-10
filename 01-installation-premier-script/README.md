# Installer un serveur web et afficher une première page PHP

À la fin de ce TP, vous saurez :

- installer un serveur web local avec PHP (WampServer, XAMPP ou Apache) et le démarrer ;
- retrouver la racine du serveur et dire à quoi elle sert ;
- afficher dans un navigateur une page PHP à partir de son adresse ;
- expliquer le rôle des balises `<?php` et `?>` ;
- lire deux erreurs : le code 404 et l'erreur de syntaxe.

Prérequis : un navigateur web et un éditeur de texte brut, par exemple Visual Studio Code, Notepad++ ou nano. Un traitement de texte comme Word ne convient pas.

> [!NOTE]
> Version utilisée
>
> Les résultats de ce cours viennent de PHP 8.4.27 et d'Apache 2.4.52, exécutés sous Ubuntu 22.04. Les numéros de version et certains messages peuvent différer sur votre machine.

## Pourquoi un serveur web ?

Un script PHP ne s'exécute pas dans le navigateur : il s'exécute sur un **serveur web**, un programme qui attend les demandes des navigateurs et y répond. Pour travailler, vous installez ce serveur sur votre propre machine : on parle de serveur **local**. Votre navigateur lui envoie une demande, le serveur exécute le script PHP, puis renvoie le résultat, que le navigateur affiche.

Le TP 02 explique cet échange en détail. Ce TP sert à installer le serveur et à voir un premier résultat.

## Installer le serveur

Dans les trois cas ci-dessous, l'installation fournit **Apache**, le programme serveur web utilisé dans ce cours, et **PHP**. Vous n'avez rien d'autre à installer et aucun réglage du `PATH` à faire. WampServer et XAMPP installent aussi un serveur de base de données, que ce cours n'utilise pas encore.

### Sous Windows : WampServer

1. Téléchargez WampServer depuis son site officiel, puis lancez l'installateur. Gardez le dossier d'installation proposé, `C:\wamp64`.
2. Lancez WampServer depuis le menu Démarrer. Une icône apparaît dans la **zone de notification**, à droite de la barre des tâches, près de l'horloge.
3. Attendez que l'icône devienne verte : verte signifie que tous les services tournent. Tant qu'elle n'est pas verte, au moins un service n'est pas démarré.
4. Faites un clic gauche sur l'icône, puis choisissez « Localhost » : le navigateur ouvre `http://localhost/`.

> [!NOTE]
> XAMPP à la place de WampServer
>
> 1. Téléchargez XAMPP sur <https://www.apachefriends.org/> et installez-le dans `C:\xampp`, pas dans `C:\Program Files` : Windows y limite l'écriture.
> 2. Ouvrez le **XAMPP Control Panel** (le programme `xampp-control.exe`) et cliquez sur le bouton « Start » de la ligne Apache.
> 3. Ouvrez `http://localhost/` : la page d'accueil de XAMPP s'affiche.
> 4. La racine du serveur est `C:\xampp\htdocs`.

### Sous Linux (Debian, Ubuntu) : Apache

Un **terminal** est une fenêtre dans laquelle on tape des commandes. Une **commande** est un ordre écrit, que l'on valide avec la touche Entrée. `sudo` donne à une commande les droits d'administrateur. `apt` télécharge et installe les logiciels, appelés « paquets ».

```bash
sudo apt update
sudo apt install apache2 libapache2-mod-php
```

- `sudo apt update` met à jour la liste des paquets disponibles.
- `sudo apt install apache2 libapache2-mod-php` installe Apache et son module PHP : le **module** est l'extension qui permet à Apache d'exécuter du PHP.

> [!WARNING]
> Le serveur ne démarre pas
>
> Un **port** est le numéro de la « porte » par laquelle un programme reçoit les demandes. Les serveurs web utilisent par défaut le port 80, et un seul programme à la fois peut l'occuper. Si le serveur ne démarre pas, un autre programme l'utilise peut-être déjà : un autre serveur web, comme IIS sous Windows, ou le logiciel Skype. Arrêtez ce programme, puis démarrez à nouveau le serveur.

## Vérifier que le serveur répond

Ouvrez `http://localhost/` dans votre navigateur. Une page d'accueil du serveur s'affiche : son contenu dépend du logiciel installé. Si le navigateur affiche à la place une erreur de connexion, le serveur n'est pas démarré : reprenez les étapes de démarrage ci-dessus.

Une adresse web s'appelle une **URL**. Elle indique où se trouve une ressource et comment l'obtenir. Prenons l'URL `http://localhost/tp01/premier.php`, que vous utiliserez dans un instant.

| Partie | Dans l'exemple | Rôle |
| --- | --- | --- |
| protocole | `http://` | le mécanisme utilisé pour obtenir la ressource |
| nom d'hôte | `localhost` | la machine où fonctionne le serveur ; `localhost` désigne votre propre machine |
| chemin | `/tp01/premier.php` | l'emplacement de la ressource sur le serveur |

## La racine du serveur : où ranger ses fichiers

Le serveur ne publie pas tout le disque de la machine : il part d'un seul dossier, la **racine du serveur**. Le chemin d'une URL se lit à partir de cette racine.

| Serveur | Racine du serveur | Pour l'ouvrir |
| --- | --- | --- |
| WampServer | `C:\wamp64\www` | clic gauche sur l'icône, puis « Dossier www » |
| XAMPP | `C:\xampp\htdocs` | explorateur de fichiers Windows |
| Apache sous Linux | `/var/www/html` | terminal ou gestionnaire de fichiers |

La racine sert à deux choses :

- **Elle limite ce que le web peut voir.** Seuls les fichiers placés dans la racine, et dans ses sous-dossiers, peuvent être demandés par un navigateur. Vos documents personnels, rangés ailleurs sur le disque, restent invisibles. C'est comme la vitrine d'un magasin : les passants voient ce qui est exposé, pas l'arrière-boutique.
- **Elle donne un sens à l'URL.** Le chemin `/tp01/premier.php` désigne le fichier `premier.php` du dossier `tp01`, situé dans la racine : `C:\wamp64\www\tp01\premier.php` avec WampServer.

Ouvrez la racine de votre serveur, puis créez dans cette racine un dossier `tp01`. Sous Linux, si le système vous refuse l'accès, utilisez `sudo` devant la commande :

```bash
sudo mkdir /var/www/html/tp01
```

> [!WARNING]
> Ouvrir le fichier directement
>
> Si l'adresse affichée dans la barre du navigateur commence par `file://` ou par `C:\`, vous avez ouvert le fichier directement, sans passer par le serveur : PHP n'est pas exécuté et vous n'obtenez pas le résultat du script. L'adresse doit toujours commencer par `http://localhost`.

## Écrire le premier script

Un **script** est un fichier texte qui contient des instructions pour PHP. Dans votre éditeur de texte, créez un fichier qui contient le code ci-dessous, et **enregistrez-le dans le dossier `tp01`** de la racine, sous le nom `premier.php`. Sous Linux, vous pouvez utiliser `sudo nano /var/www/html/tp01/premier.php`.

```php
<?php
echo "Bonjour";
?>
```

- Ligne 1 : `<?php` ouvre le code PHP.
- Ligne 2 : `echo` est une **instruction** qui affiche du texte. `"Bonjour"` est une **chaîne de caractères** : un texte écrit entre guillemets droits. Le point-virgule `;` termine l'instruction.
- Ligne 3 : `?>` ferme le code PHP.

**Prédisez** ce que le navigateur va afficher : le code du script ou son résultat ? Ouvrez ensuite `http://localhost/tp01/premier.php`.

Vous devez voir, dans la page :

```text
Bonjour
```

Le navigateur affiche le résultat du script, pas son code : c'est le serveur qui a exécuté PHP.

Après chaque modification d'un fichier, enregistrez-le avec Ctrl+S, puis rechargez la page dans le navigateur avec la touche F5.

> [!WARNING]
> Un nom de fichier qui se termine par .txt
>
> Avec Windows, l'explorateur de fichiers peut cacher les extensions. Un fichier enregistré sous le nom `premier.php` peut alors s'appeler en réalité `premier.php.txt`. Le serveur cherche `premier.php`, ne le trouve pas et répond par l'erreur 404, étudiée dans la section suivante. Activez l'affichage des extensions de noms de fichiers dans le menu « Affichage » de l'explorateur, puis renommez le fichier.

## Lire une erreur 404

**Modifiez une seule chose.** Dans votre explorateur de fichiers, déplacez `premier.php` du dossier `tp01` vers la racine du serveur. Ce changement place le fichier un niveau plus haut que ne l'indique l'URL.

**Prédisez** ce que le navigateur va afficher, puis rechargez `http://localhost/tp01/premier.php` avec la touche F5.

Vous devez voir, avec Apache sous Linux :

```text
Not Found

The requested URL was not found on this server.
```

Le texte exact de la page d'erreur dépend du serveur. Le **code 404** signifie « ressource introuvable » : le serveur a cherché le fichier `tp01/premier.php` dans la racine et ne l'y a pas trouvé. L'URL doit désigner l'endroit exact où se trouve le fichier.

Vérifiez-le : ouvrez maintenant `http://localhost/premier.php`. Cette URL désigne le fichier à la racine, et la page affiche `Bonjour`.

Remettez ensuite `premier.php` dans le dossier `tp01`.

## Modifier le script, une chose à la fois

**Modifiez une seule chose.** Ajoutez une ligne 3 : `echo "tout le monde";`. Cette ligne demande à PHP d'afficher un second texte.

```php
<?php
echo "Bonjour";
echo "tout le monde";
?>
```

**Prédisez** : y a-t-il un espace entre `Bonjour` et `tout` ? Enregistrez, puis rechargez la page.

Vous devez voir, dans la page :

```text
Bonjourtout le monde
```

`echo` n'ajoute pas d'espace : il affiche seulement ce qui se trouve entre les guillemets.

**Modifiez une seule chose.** Ligne 2, ajoutez un espace avant le guillemet fermant : `"Bonjour "` au lieu de `"Bonjour"`. Ce changement ajoute un espace au texte affiché.

```php
<?php
echo "Bonjour ";
echo "tout le monde";
?>
```

**Prédisez**, enregistrez, puis rechargez la page.

Vous devez voir, dans la page :

```text
Bonjour tout le monde
```

## À quoi servent `<?php` et `?>`

Le serveur envoie tel quel ce qui se trouve en dehors des balises, et exécute ce qui se trouve entre `<?php` et `?>`. Vérifiez-le : créez dans `tp01` un fichier `balises.php` qui contient du texte avant et après le code, sur une seule ligne.

```php
Avant <?php echo "milieu"; ?> Après
```

**Prédisez** ce qui va s'afficher, puis ouvrez `http://localhost/tp01/balises.php`.

Vous devez voir, dans la page :

```text
Avant milieu Après
```

- `Avant` et `Après` sont en dehors des balises : le serveur les envoie sans les modifier.
- `milieu` vient de l'instruction placée entre `<?php` et `?>`.

> [!WARNING]
> Lettres accentuées illisibles
>
> Si `Après` s'affiche avec un caractère étrange à la place du `è`, votre fichier n'est pas enregistré en UTF-8. Dans votre éditeur, choisissez l'encodage « UTF-8 » (Visual Studio Code l'affiche en bas à droite, Notepad++ dans le menu « Encodage »), puis enregistrez à nouveau le fichier.

## Vérifier la version de PHP

La fonction `phpinfo()` génère une page qui décrit la configuration de PHP. Dans `tp01`, créez un fichier `phpinfo.php` :

```php
<?php phpinfo(); ?>
```

**Prédisez** ce que la page va afficher en haut, puis ouvrez `http://localhost/tp01/phpinfo.php`.

Vous devez voir, en haut de la page, avec PHP 8.4.27 :

```text
PHP Version 8.4.27
```

Votre numéro de version peut différer : dans `8.4.27`, 8 est la version majeure, 4 la version mineure et 27 le correctif.

La page contient aussi la ligne « Loaded Configuration File », qui donne le chemin du fichier de réglages de PHP, appelé `php.ini`. Cherchez dans la page la ligne `display_errors` (touches Ctrl+F). Elle contient deux colonnes : la première, « Local Value », est la valeur utilisée par le serveur. Sur la machine de rédaction, la ligne est :

```text
display_errors   Off   Off
```

`display_errors` décide si PHP affiche ses messages d'erreur dans la page. Relevez la valeur sur votre machine : la section suivante en dépend.

## Lire une erreur de syntaxe

Une **erreur de syntaxe** est une instruction écrite de travers, que PHP ne peut pas lire.

**Modifiez une seule chose.** Dans `premier.php`, ligne 2, supprimez le point-virgule à la fin de l'instruction : `echo "Bonjour "` au lieu de `echo "Bonjour ";`. Ce changement supprime la fin de l'instruction.

```php
<?php
echo "Bonjour "
echo "tout le monde";
?>
```

**Prédisez** : la page va-t-elle afficher `Bonjour` avant de s'arrêter ? Enregistrez, puis rechargez `http://localhost/tp01/premier.php`.

**Si `display_errors` vaut `On`**, vous devez voir, dans la page :

```text
Parse error: syntax error, unexpected token "echo", expecting "," or ";" in …/tp01/premier.php on line 3
```

Les points de suspension `…` remplacent le début du chemin, qui dépend de votre machine. Lisez le message :

- `Parse error` : erreur d'analyse du code. PHP lit tout le fichier avant de l'exécuter. Il refuse ce fichier, donc aucun texte n'est affiché.
- `syntax error, unexpected token "echo"` : erreur de syntaxe. PHP rencontre un `echo` là où il ne l'attendait pas.
- `expecting "," or ";"` : à cet endroit, PHP attendait une virgule ou un point-virgule.
- `in …/tp01/premier.php` : le fichier concerné.
- `on line 3` : la ligne où PHP s'est arrêté. C'est la ligne qui suit l'oubli : PHP ne voit le point-virgule manquant qu'en lisant le `echo` suivant.

Dans la page, les mots « Parse error », le chemin du fichier et le numéro de ligne sont en gras : PHP a écrit son message en HTML. Le TP 02 explique ce que cela signifie.

**Si `display_errors` vaut `Off`**, la page reste vide et le serveur répond par le code 500, « erreur interne du serveur ». Le message n'est pas perdu : le serveur l'écrit dans son journal d'erreurs, mais vous ne le voyez pas dans la page. Pour apprendre, il vaut mieux l'afficher :

1. Dans la page `phpinfo.php`, relevez le chemin de la ligne « Loaded Configuration File » : c'est le fichier `php.ini` que le serveur utilise.
2. Ouvrez ce fichier avec votre éditeur (sous Linux, avec `sudo`), cherchez la ligne `display_errors`, et remplacez sa valeur par `On`.
3. Enregistrez le fichier, puis redémarrez Apache : avec WampServer ou XAMPP, utilisez le menu de l'icône ou le panneau de contrôle ; sous Linux, tapez `sudo systemctl restart apache2`.
4. Rechargez `phpinfo.php` : `display_errors` doit maintenant valoir `On`. Rechargez ensuite `premier.php`.

Remettez le point-virgule à la fin de la ligne 2.

## Écrire un commentaire

Un **commentaire** est un texte écrit pour les humains, que PHP ignore. Il commence par `//` et s'arrête à la fin de la ligne. Pour plusieurs lignes, on l'écrit entre `/*` et `*/`.

**Modifiez une seule chose.** Ajoutez une ligne 2 : `// Mon premier script`. Cette ligne est un commentaire : elle n'ajoute rien à ce que PHP exécute.

```php
<?php
// Mon premier script
echo "Bonjour ";
echo "tout le monde";
?>
```

**Prédisez**, enregistrez, puis rechargez la page.

Vous devez voir, dans la page :

```text
Bonjour tout le monde
```

**Modifiez une seule chose.** Ligne 4, ajoutez `// ` au début de l'instruction : `// echo "tout le monde";`. Ce changement transforme l'instruction en commentaire : PHP ne l'exécute plus.

```php
<?php
// Mon premier script
echo "Bonjour ";
// echo "tout le monde";
?>
```

**Prédisez**, enregistrez, puis rechargez la page.

Vous devez voir, dans la page :

```text
Bonjour
```

## Exercice

Dans `tp01`, créez un fichier `identite.php` qui affiche, sur une seule ligne et avec deux instructions `echo`, ce texte :

```text
Nom : Dupont Prénom : Léa
```

Ouvrez `http://localhost/tp01/identite.php` et comparez avec le texte ci-dessus.
