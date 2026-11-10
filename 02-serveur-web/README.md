# Le serveur web : une page PHP dans le navigateur

À la fin de ce TP, vous saurez :

- décrire le rôle du client et du serveur quand on demande une page PHP ;
- lire une URL et dire à quel fichier du serveur elle correspond ;
- afficher dans un navigateur une page PHP enregistrée à la racine du serveur ;
- lire dans le navigateur la méthode et le code de statut HTTP d'une requête ;
- mélanger du HTML et du PHP dans un même fichier.

Prérequis : le chapitre 1, et un serveur Apache avec PHP (installé dans la section « Installer le serveur »).

## Le client et le serveur

La connexion et l'échange de données entre un navigateur web et un serveur web reposent sur l'architecture **client/serveur** :

- le **client** est le navigateur web. Il envoie une **requête** à un serveur ;
- le **serveur** est un programme (Apache, Nginx, IIS, Tomcat…) qui fonctionne sur une machine. Il reçoit les requêtes et y répond par une **réponse** ;
- le protocole **HTTP** (*HyperText Transfer Protocol*) décrit comment le client et le serveur s'échangent ces messages.

Le **HTML** (*HyperText Markup Language*) est un langage qui décrit une page web. Une page HTML enregistrée sur le serveur est **statique** : le serveur l'envoie telle quelle, à chaque demande. Prenons un site marchand : un utilisateur doit pouvoir choisir un produit, le mettre dans son panier, puis afficher son panier pour voir la somme de ses achats. Le résultat est **dynamique** : le serveur doit fabriquer les pages à la volée. C'est là que PHP intervient.

PHP signifie *Hypertext Preprocessor*. C'est un langage dédié à la création de pages dynamiques. Un script PHP est exécuté du côté du serveur, par l'interpréteur PHP. Le navigateur n'exécute jamais de PHP : le serveur lui envoie seulement le résultat du script.

## Que se passe-t-il quand on demande une page PHP ?

Voici le cheminement d'une demande, du navigateur jusqu'à l'affichage de la page :

1. Le navigateur web émet une requête à partir d'une URL. Cette URL contient le nom du serveur et de la ressource demandée (un fichier PHP).
2. Le serveur HTTP reçoit la requête et vérifie si la ressource (le fichier PHP) existe.
3. Le serveur HTTP accède au fichier PHP.
4. Le contenu du fichier PHP est transmis à l'interpréteur PHP pour être exécuté.
5. Si le script utilise une base de données, l'interpréteur PHP ouvre une connexion avec le serveur de base de données et lui transmet une requête SQL.
6. Le SGBD (système de gestion de base de données) traite la requête SQL et transmet le résultat.
7. Une fois le script PHP exécuté, le code HTML généré est transmis au serveur HTTP, qui l'encapsule pour qu'il soit transportable.
8. La réponse HTTP, qui contient le code HTML, passe du réseau au navigateur.
9. Le navigateur réceptionne le code généré et interprète le code HTML.

Les étapes 5 et 6 n'ont lieu que pour un script qui utilise une base de données : ce cours n'en utilise pas encore. Sans elles, le schéma se résume ainsi :

```text
Navigateur  --- 1. requête HTTP --->  Serveur HTTP (Apache)
                                         |  2. le fichier PHP est confié à
                                         v
                                      Interpréteur PHP
                                         |  3. le script s'exécute et produit du HTML
                                         v
Navigateur  <--- 4. réponse HTTP ---  Serveur HTTP (Apache)
```

## Installer le serveur

Sous Linux (Debian, Ubuntu), installez Apache et son module PHP :

```bash
sudo apt update
sudo apt install apache2 libapache2-mod-php
```

Pour vérifier que le serveur fonctionne, ouvrez `http://localhost` dans un navigateur : si une page s'affiche, le serveur répond.

## Comprendre l'URL

Une **URL** indique où se trouve une ressource et comment l'obtenir. Prenons l'URL `http://localhost/tp02/bonjour.php`.

| Partie | Dans l'exemple | Rôle |
| --- | --- | --- |
| protocole | `http://` | le mécanisme utilisé pour obtenir la ressource |
| nom d'hôte | `localhost` | la machine où fonctionne le serveur ; `localhost` désigne votre propre machine |
| chemin | `/tp02/bonjour.php` | l'emplacement de la ressource sur le serveur |

Le serveur ne montre pas tous les fichiers de la machine : il part d'un dossier appelé la **racine du serveur**. Sous Linux, c'est `/var/www/html` avec une installation d'Apache par défaut. Le chemin d'une URL se lit à partir de cette racine : `/tp02/bonjour.php` correspond au fichier `/var/www/html/tp02/bonjour.php`. Sous Windows, c'est le dossier indiqué par la directive `DocumentRoot` de la configuration d'Apache. Quand l'URL ne contient pas de nom de fichier, le serveur cherche en général un fichier `index.html` ou `index.php` dans le dossier.

## Créer une première page

Dans la racine du serveur, créez un dossier `tp02`. Sous Linux, si le système vous refuse l'accès, utilisez `sudo` devant la commande :

```bash
sudo mkdir /var/www/html/tp02
```

Dans `/var/www/html/tp02`, créez un fichier `bonjour.php`. Sous Linux, vous pouvez utiliser `sudo nano /var/www/html/tp02/bonjour.php` ; sous Windows, utilisez un éditeur de texte comme Notepad++.

```php
<?php
echo "Bonjour depuis le serveur";
?>
```

**Prédisez** ce que le navigateur va afficher : le code du script ou son résultat ? Ouvrez ensuite `http://localhost/tp02/bonjour.php` dans le navigateur.

Le navigateur affiche :

```text
Bonjour depuis le serveur
```

Pour voir ce que le serveur a réellement envoyé, affichez le code source de la page avec les touches Ctrl+U.

Vous devez voir :

```text
Bonjour depuis le serveur
```

Le navigateur n'a reçu que le résultat. Il ne contient aucune trace de `echo` ni de `<?php` : le code PHP est resté sur le serveur, aux étapes 3 et 4 du cheminement.

## Lire la méthode et le code de statut HTTP

Chaque requête du navigateur a une **méthode** : `GET` signifie « donne-moi cette ressource ». Chaque réponse du serveur contient un **code de statut**, un nombre à trois chiffres qui indique si la requête a réussi. Le navigateur les affiche dans son inspecteur, appelé aussi « devtools » :

1. Ouvrez l'inspecteur avec la touche F12, puis l'onglet « Réseau » (« Network » dans Chrome).
2. Rechargez la page `http://localhost/tp02/bonjour.php` avec la touche F5.
3. Une ligne apparaît dans l'onglet : c'est la requête que le navigateur vient d'envoyer.

Pour de l'aide sur l'inspecteur, consultez la documentation de [Firefox](https://firefox-source-docs.mozilla.org/devtools-user/index.html) ou de [Chrome](https://developer.chrome.com/docs/devtools/open/).

**Prédisez** la méthode et le code de statut de cette requête.

Vous devez voir, dans les colonnes de l'onglet Réseau de Firefox :

```text
État   Méthode   Domaine     Fichier
200    GET       localhost   bonjour.php
```

La méthode est `GET`. Le code `200` signifie que la requête a réussi : le serveur a trouvé le fichier et il a répondu.

## Lire un code d'erreur : 404

**Modifiez une seule chose.** Dans la barre d'adresse, remplacez `bonjour.php` par `inexistant.php`. Ce changement désigne un fichier qui n'existe pas dans le dossier `tp02`.

**Prédisez** le code de statut, puis validez l'adresse.

Le navigateur affiche :

```text
Not Found

The requested URL was not found on this server.
```

Vous devez voir, dans l'onglet Réseau :

```text
État   Méthode   Domaine     Fichier
404    GET       localhost   inexistant.php
```

Le code `404` signifie « ressource introuvable » : l'URL désigne un fichier qui n'existe pas à cet endroit de la racine du serveur. Le texte de la page d'erreur signifie « introuvable : l'adresse demandée n'existe pas sur ce serveur ». Le code `200` de la section précédente signifie au contraire que la ressource a été trouvée.

## Mélanger HTML et PHP

Le navigateur lit du HTML, et le serveur peut fabriquer du HTML avec PHP. Dans `/var/www/html/tp02`, créez un fichier `page.php` qui contient à la fois du HTML et du PHP :

```php
<html>
<body>
<p>2 + 3 = <?php echo 2 + 3; ?></p>
</body>
</html>
```

- Les lignes 1, 2, 4 et 5 sont du HTML, en dehors des balises PHP : le serveur les envoie telles quelles.
- La ligne 3 contient du PHP entre `<?php` et `?>`, comme au chapitre 1 : le serveur le remplace par son résultat.

**Prédisez** ce que le navigateur va afficher, puis ouvrez `http://localhost/tp02/page.php`.

Le navigateur affiche :

```text
2 + 3 = 5
```

Affichez le code source de la page avec les touches Ctrl+U.

Vous devez voir :

```text
<html>
<body>
<p>2 + 3 = 5</p>
</body>
</html>
```

Le navigateur n'affiche pas les balises HTML : il les interprète pour construire la page. Le calcul `2 + 3` a été fait par PHP sur le serveur, avant l'envoi.

**Modifiez le fichier `page.php`** : remplacez tout son contenu par le script suivant. Le HTML est maintenant écrit par le code PHP.

```php
<?php
echo "<html><p>Bonjour</p></html>";
?>
```

**Prédisez** ce que le navigateur va afficher, puis rechargez la page.

Le navigateur affiche :

```text
Bonjour
```

Le code source de la page, avec Ctrl+U, est maintenant :

```text
<html><p>Bonjour</p></html>
```

On peut donc mettre du PHP dans du HTML, ou du HTML dans du PHP : dans les deux cas, le navigateur reçoit du HTML.

## Afficher la configuration de PHP

La fonction `phpinfo()` génère une page qui décrit la configuration de PHP. Dans `/var/www/html/tp02`, créez un fichier `phpinfo.php` :

```php
<?php phpinfo(); ?>
```

Ouvrez `http://localhost/tp02/phpinfo.php` dans le navigateur : la page affiche la version de PHP, les extensions chargées et les réglages du fichier `php.ini`.

**Prédisez** la version de PHP affichée en haut de la page.

Vous devez voir, en haut de la page, avec PHP 8.4.27 :

```text
PHP Version 8.4.27
```

Votre numéro de version peut différer.
