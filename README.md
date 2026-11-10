# Introduction à PHP

Cours d'introduction à la programmation avec PHP pour des élèves qui découvrent la programmation : BTS SIO, 1ʳᵉ année (tronc commun SISR et SLAM). Chaque TP se fait en prédisant le résultat, en l'affichant dans le navigateur, puis en comparant.

## TP

| TP | Sujet |
| --- | --- |
| [1](01-installation-premier-script/README.md) | Installer un serveur web et afficher une première page PHP |
| [2](02-serveur-web/README.md) | Le client et le serveur : ce que le navigateur reçoit |
| [3](03-variables-texte-nombres/README.md) | Les variables : texte et nombres |
| [4](04-calculs-et-mise-a-jour/README.md) | Calculer et mettre à jour une variable |
| [5](05-tableaux/README.md) | Les tableaux |
| [6](06-comparer-et-decider/README.md) | Comparer et décider |
| [7](07-boucles/README.md) | Répéter avec les boucles |
| [8](08-fonctions/README.md) | Écrire ses propres fonctions |
| [9](09-formulaires-get-post/README.md) | Les formulaires : envoyer des données avec GET et POST |
| [10](10-tp-notes-csv/README.md) | Les notes des étudiants avec un fichier CSV |
| [11](11-tp-notes-json/README.md) | Les notes des étudiants avec un fichier JSON |

## Télécharger les PDF

Chaque TP existe aussi en PDF, avec un sommaire cliquable, des signets pour naviguer dans le volet latéral du lecteur et des liens internes. Les fichiers sont régénérés automatiquement à chaque mise à jour du cours et publiés dans la release [pdf-latest](https://github.com/ornech/SIO1-PHP/releases/tag/pdf-latest) : un PDF par TP, nommé comme le dossier du TP (par exemple `03-variables-texte-nombres.pdf`). Pour les générer en local, voir l'en-tête de `outils/pdf.py`.

Prérequis : un navigateur web et un éditeur de texte brut. Le TP 1 installe le serveur Apache avec PHP (WampServer ou XAMPP sous Windows, Apache sous Linux) : les scripts du cours s'affichent tous dans le navigateur.

Versions de référence (celles qui ont servi à exécuter les exemples du cours) :

- PHP : 8.4.27
- Apache : 2.4.52

## Auteur, licence et assistance de l'IA

**Auteur :** Jean-François ORNECH, enseignant.

**Licence :** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr) : attribution, pas d'utilisation commerciale, partage dans les mêmes conditions.

**Assistance de l'IA.** Ce document a été conçu et validé par son auteur, avec l'assistance de l'IA Claude (Anthropic) : rejeu des scénarios, pertinence des tests, relecture et rédaction de compléments.

**Versions.** Le cours est numéroté par des tags Git (`v1.0`, `v1.1`…). Le numéro de version et le commit figurent sur la page de garde et en pied de page de chaque PDF.
