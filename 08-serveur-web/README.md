# Le serveur web : une page PHP dans le navigateur

À la fin de ce TP, vous saurez :

- décrire les trois parties d'une URL ;
- placer un fichier PHP à la racine du serveur et l'ouvrir dans un navigateur ;
- expliquer pourquoi le navigateur reçoit le résultat du script et jamais son code ;
- mélanger du HTML et du PHP dans un même fichier ;
- lire un code de statut HTTP, dont le code 404.

Prérequis : les chapitres 1 et 2, et un serveur Apache avec PHP installé.

## Installer le serveur

Un **navigateur** demande des pages à un **serveur web**. Le serveur web est un programme, ici Apache, qui répond à ces demandes. Il sait aussi demander à PHP d'exécuter un script avant de répondre.

Sous Linux (Debian, Ubuntu), installez Apache et son module PHP :

```bash
sudo apt update
sudo apt install apache2 libapache2-mod-php
```

Pour vérifier que le serveur fonctionne, ouvrez `http://localhost` dans un navigateur : si une page s'affiche, le serveur répond.

## Comprendre l'URL

Une **URL** indique où se trouve une ressource et comment l'obtenir. Prenons l'URL `http://localhost/tp08/bonjour.php`.

| Partie | Dans l'exemple | Rôle |
| --- | --- | --- |
| protocole | `http://` | le mécanisme utilisé pour obtenir la ressource |
| nom d'hôte | `localhost` | la machine où fonctionne le serveur ; `localhost` désigne votre propre machine |
| chemin | `/tp08/bonjour.php` | l'emplacement de la ressource sur le serveur |

Le serveur ne montre pas tous les fichiers de la machine : il part d'un dossier appelé la **racine du serveur**. Sous Linux, c'est `/var/www/html` avec une installation d'Apache par défaut. Le chemin d'une URL se lit à partir de cette racine : `/tp08/bonjour.php` correspond au fichier `/var/www/html/tp08/bonjour.php`. Sous Windows, c'est le dossier indiqué par la directive `DocumentRoot` de la configuration d'Apache.

## Créer une première page

Dans la racine du serveur, créez un dossier `tp08`. Sous Linux, si le système vous refuse l'accès, utilisez `sudo` devant la commande :

```bash
sudo mkdir /var/www/html/tp08
```

Dans `/var/www/html/tp08`, créez un fichier `bonjour.php`. Sous Linux, vous pouvez utiliser `sudo nano /var/www/html/tp08/bonjour.php` ; sous Windows, utilisez un éditeur de texte comme Notepad++.

```php
<?php
echo "Bonjour depuis le serveur\n";
?>
```

**Prédisez** ce que le navigateur va afficher : le code du script ou son résultat ? Ouvrez ensuite `http://localhost/tp08/bonjour.php` dans le navigateur.

Le navigateur affiche :

```text
Bonjour depuis le serveur
```

Vérifiez ce que le serveur envoie réellement, sans passer par le navigateur. La commande `curl` envoie une requête et affiche la réponse :

```bash
curl http://localhost/tp08/bonjour.php
```

Vous devez voir :

```text
Bonjour depuis le serveur
```

Le serveur a confié le fichier à PHP, puis il a renvoyé seulement le résultat. Le code PHP ne quitte jamais le serveur : ni le navigateur ni `curl` n'y ont accès.

## Lire la réponse HTTP

Le navigateur et le serveur communiquent avec le protocole **HTTP**. Le navigateur envoie une **requête** (« donne-moi `/tp08/bonjour.php` »), le serveur renvoie une **réponse**. L'option `-i` de `curl` affiche aussi l'en-tête de la réponse :

```bash
curl -i http://localhost/tp08/bonjour.php
```

**Prédisez** la première ligne de la réponse, puis exécutez la commande.

Vous devez voir :

```text
HTTP/1.1 200 OK
Date: …
Server: Apache/2.4.52 (Ubuntu)
Content-Length: 26
Content-Type: text/html; charset=UTF-8

Bonjour depuis le serveur
```

- `HTTP/1.1 200 OK` : la version du protocole, puis le **code de statut** `200`, qui signifie « la requête a réussi ».
- `Date: …` : la date de la réponse. Elle change à chaque exécution, et le texte `…` la remplace ici.
- `Server: Apache/2.4.52 (Ubuntu)` : le serveur qui répond. Votre version peut différer.
- `Content-Length: 26` : la taille de la réponse en octets (le texte `Bonjour depuis le serveur` et son retour à la ligne).
- `Content-Type: text/html; charset=UTF-8` : le type du contenu envoyé.
- La ligne vide sépare l'en-tête du contenu, qui vient ensuite.

## Lire un code d'erreur : 404

**Modifiez une seule chose.** Demandez un fichier qui n'existe pas : remplacez `bonjour.php` par `inexistant.php` dans l'URL. L'option `-w` demande à `curl` d'afficher le code de statut, `-s` supprime les messages de progression et `-o /dev/null` jette le contenu de la réponse.

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/tp08/inexistant.php
```

**Prédisez** le code de statut, puis exécutez la commande.

Vous devez voir :

```text
404
```

Le code `404` signifie « ressource introuvable » : l'URL désigne un fichier qui n'existe pas à cet endroit de la racine du serveur. Le navigateur affiche alors une page d'erreur. Le code `200` de la section précédente signifie au contraire que la ressource a été trouvée.

## Mélanger HTML et PHP

Un navigateur lit du **HTML**, un langage qui décrit une page avec des balises. Le serveur peut fabriquer du HTML avec PHP. Dans `/var/www/html/tp08`, créez un fichier `page.php` qui contient du HTML et du PHP :

```php
<html>
<body>
<p>2 + 3 = <?php echo 2 + 3; ?></p>
</body>
</html>
```

- Les lignes 1, 2, 4 et 5 sont du HTML, en dehors des balises PHP : le serveur les envoie telles quelles.
- La ligne 3 contient du PHP entre `<?php` et `?>`, comme au chapitre 1 : le serveur le remplace par son résultat.

**Prédisez** le texte envoyé par le serveur, puis exécutez la commande :

```bash
curl http://localhost/tp08/page.php
```

Vous devez voir :

```text
<html>
<body>
<p>2 + 3 = 5</p>
</body>
</html>
```

Le navigateur n'affiche pas les balises : il affiche une page avec le texte `2 + 3 = 5`. Ouvrez `http://localhost/tp08/page.php` pour le vérifier.

**Modifiez le fichier `page.php`** : remplacez tout son contenu par le script suivant. Le HTML est maintenant écrit par le code PHP.

```php
<?php
echo "<html><p>Bonjour</p></html>\n";
?>
```

**Prédisez** le texte envoyé, puis exécutez la même commande `curl`.

```bash
curl http://localhost/tp08/page.php
```

Vous devez voir :

```text
<html><p>Bonjour</p></html>
```

On peut donc mettre du PHP dans du HTML, ou du HTML dans du PHP : dans les deux cas, le navigateur reçoit du HTML.

## Afficher la configuration de PHP

La fonction `phpinfo()` génère une page qui décrit la configuration de PHP. Dans `/var/www/html/tp08`, créez un fichier `phpinfo.php` :

```php
<?php phpinfo(); ?>
```

Ouvrez `http://localhost/tp08/phpinfo.php` dans le navigateur : la page affiche la version de PHP, les extensions chargées et les réglages du fichier `php.ini`.

**Prédisez** la version affichée en haut de la page, puis cherchez-la dans la réponse du serveur :

```bash
curl -s http://localhost/tp08/phpinfo.php | grep -o "PHP Version [0-9.]*" | head -1
```

Vous devez voir, avec PHP 8.4.27 :

```text
PHP Version 8.4.27
```

Votre numéro de version peut différer.
