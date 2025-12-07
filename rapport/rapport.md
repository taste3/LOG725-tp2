<div style='text-align: center; line-height:3rem; font-size:1.5rem; font-weight: 500; font-family: Calibri;'>
<div style="height:60px;"></div>
Travail Pratique 2
<div style="height:80px;"></div>
par
<div style="height:80px;"></div>
Nicolas PATENAUDE
<div style="height:80px;"></div>
DEVOIR PRÉSENTÉ À Loïc CYR
<div style="height:80px;"></div>
LOG725-01
<div style="height:110px;"></div>
MONTRÉAL, LE 4 DÉCEMBRE 2025
<div style="height:80px;"></div>
ÉCOLE DE TECHNOLOGIE SUPÉRIEURE
<div style="height:0px;"></div>
UNIVERSITÉ DU QUÉBEC
</div>
<div style="page-break-before: always;"></div>

# Présentation

Pour ce travail, j'ai fait un réusinage du projet "Myriapod" que j'ai trouvé dans un des Repo GitHub recommendé dans l'énoncé du travail: <a href="https://github.com/Wireframe-Magazine/Code-the-Classics">https://github.com/Wireframe-Magazine/Code-the-Classics</a>
Le travail est accessible sur mon répertoire git (publique): <a href="https://github.com/taste3/LOG725-tp2">https://github.com/taste3/LOG725-tp2</a>. Dans ce jeu, on contrôle un petit robot et on tire sur des roches et sur un myriapode (mille-pattes) robotisé.

Les instructions pour lancer le jeu sont disponible dans le fichier README du projet et sont lisibles sur la page d'accueil de mon GitHub.

# Modifications

Tout séparé de une seule grosse classe monolithe en différentes classes qui représentent des entitées (conteneurs). Si le jeu était complètement refactoré avec le patron ECS, c'est entitées devraient être encore plus séparés
Retiré le système de son du jeu de l'instance du jeu, la fonction qui permet de faire jouer un son utilise l'instance du jeu, mais n'est pas contenue dans cette instance.

# Patrons

Patron Singleton pour l'instance de jeu globale

# Diagramme de classes

Le diagramme de classes suivant à été abrégé pour qu'il reste lisible et compréhensible, il ne contient pas toute les méthodes et attributs de toutes les classes, seulement ce qui est pertinent aux relations entre les classes et à leurs fonctionnements.

![Diagramme de classes](.\LOG725-tp1\out\docs\diagrammes_de_classe\diagrammes_de_classe.png)



![Image porte fermée](.\LOG725-tp1\docs\porte_ferme.png)

<p align="center"><em>Figure 1 : Porte fermée avant activation du bouton</em></p>

![Image porte ouverte](.\LOG725-tp1\docs\porte_ouverte.png)

<p align="center"><em>Figure 2 : Porte ouverte après activation du bouton</em></p>