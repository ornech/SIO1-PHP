# Introduction à PHP

Cours d'introduction à la programmation avec PHP pour des élèves qui découvrent la programmation : BTS SIO, 1ʳᵉ année (tronc commun SISR et SLAM). Chaque chapitre se fait en prédisant le résultat, en exécutant le programme, puis en comparant.

## Chapitres

| Chapitre | Sujet |
| --- | --- |
| [1](01-installation-premier-script/README.md) | Installer PHP et écrire un premier script |
| [2](02-variables-texte-nombres/README.md) | Les variables : texte et nombres |
| [3](03-calculs-et-mise-a-jour/README.md) | Calculer et mettre à jour une variable |
| [4](04-tableaux/README.md) | Les tableaux |
| [5](05-comparer-et-decider/README.md) | Comparer et décider |
| [6](06-boucles/README.md) | Répéter avec les boucles |
| [7](07-fonctions/README.md) | Écrire ses propres fonctions |
| [8](08-serveur-web/README.md) | Le serveur web : une page PHP dans le navigateur |
| [9](09-formulaires-get-post/README.md) | Les formulaires : envoyer des données avec GET et POST |
| [10](10-tp-notes-csv/README.md) | TP : les notes des étudiants (fichier CSV) |
| [11](11-tp-notes-json/README.md) | TP : les notes des étudiants (fichier JSON) |

## Télécharger les PDF

Chaque chapitre existe aussi en PDF, avec un sommaire cliquable, des signets pour naviguer dans le volet latéral du lecteur et des liens internes. Les fichiers sont régénérés automatiquement à chaque mise à jour du cours et publiés dans la release [pdf-latest](https://github.com/ornech/SIO1-PHP/releases/tag/pdf-latest) : un PDF par chapitre, nommé comme le dossier du chapitre (par exemple `02-variables-texte-nombres.pdf`). Pour les générer en local, voir l'en-tête de `outils/pdf.py`.

Prérequis : PHP en ligne de commande (la commande `php -v` doit afficher une version). Les chapitres 8 à 11 demandent aussi un serveur Apache avec PHP.

Versions de référence (celles qui ont servi à exécuter les exemples du cours) :

- PHP : 8.4.27
- Apache : 2.4.52

## Auteur, licence et assistance de l'IA

**Auteur :** Jean-François ORNECH, enseignant.

**Licence :** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr) : attribution, pas d'utilisation commerciale, partage dans les mêmes conditions.

**Assistance de l'IA.** Ce document a été conçu et validé par son auteur, avec l'assistance de l'IA Claude (Anthropic) : rejeu des scénarios, pertinence des tests, relecture et rédaction de compléments.

**Versions.** Le cours est numéroté par des tags Git (`v1.0`, `v1.1`…). Le numéro de version et le commit figurent sur la page de garde et en pied de page de chaque PDF.
