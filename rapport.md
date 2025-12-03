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

# Diagramme de classes

Le diagramme de classes suivant à été abrégé pour qu'il reste lisible et compréhensible, il ne contient pas toute les méthodes et attributs de toutes les classes, seulement ce qui est pertinent aux relations entre les classes et à leurs fonctionnements.

![Diagramme de classes](.\LOG725-tp1\out\docs\diagrammes_de_classe\diagrammes_de_classe.png)

## Scenes

Il y à deux scènes, le menu principal (MainMenu) et le niveau 1 (MainScene). Le menu principal permet de lancer la partie, quitter le jeu et activer/désactiver les effets sonores et la musique à l'aide de cases à cocher. Le niveau 1 est le seul niveau du jeu, il est basé sur l'exemple donné avec une modification pour la fonctionnalité supplémentaire.

## Scripts

### MainMenu
Ce script permet la gestion des boutons et paramêtres contenus dans la scène MainMenu.
### Joueur
Le script joueur est basée sur le script fournis MouvementJoueur. Il fait la gestion des munitions, du mouvement, de ses animations de mouvement et de ses effets sonores. Lorsque la barre d'espace est appuyée, et que la munition sélectionnée est disponible, il créé un objet Bullet de la bonne couleur et lui donne une vitesse constante orienté selon l'orientation du joueur.
### AmmoBox
Lorsque le joueur entre en collision avec la boite de munition, elle disparait et une munition de la couleur associée est ajoutée au joueur.
### Bullet
Lorsque la balle entre en collision avec une un mur, elle est détruite.
### BreakableWall
Lorsque le mur entre en collision avec une balle de la même couleur, celui-ci est détruit.
### LevelManager
Le level manager permet de recommencer la partie si le joueur appuie sur la touche R.
### SoundManager
Ce script fait jouer la musique de fond dans le menu principal et dans la scène du niveau 1. Il permet également certains effets sonores associées aux niveau tel que le son de succès et le son d'ouverture d'une porte. Il va chercher dans les PlayerPrefs afin de savoir si les sons ont été activés/désactivés dans le menu principal.
### Exit
Si un joueur entre en colision avec le Exit, fait apparaitre l'écran de succès, fait jouer le son de succès et charge le menu principal.
### DoorButton
Si la bonne munition entre en collision avec le bouton, son sprite change pour indiquer son activation et la porte qui lui est associée est ouverte.
### Door
La porte peut seulement s'ouvrir. Lorsqu'elle s'ouvre, son sprite s'actualise et sa boite de collision se désactive.
### AmmoMenu
Le menu de gauche affiche le nombre de chaque type de munition du joueur. Il affiche également un indice d'appuyer sur la touche "R" afin de redémarrer la partie.

## Prefabs

Plusieurs objects qui se trouvent dans la tilemap ou qui sont répétés plusieurs fois dans le niveau sont enregistrés sous la forme de prefabs. Certains de ces prefabs sont identique à une couleur près. Plusieurs d'entre eux implémentent la méthode void OnValidate() qui permet d'afficher les bonnes couleurs directement dans l'éditeur de niveau. Sans cette méthode, les couleurs des murs et des munitions ne pourraient pas varier selon une enum de couleurs et être affichés dans la bonne couleur dans l'éditeur.

# Ajout/Modification au GDD

L'ajout effectué au GDD introduit un nouveau type d'interaction: un système de boutons et de portes. Les boutons peuvent se trouver hors de la porté des joueurs et doivent se faire percuter avec le type de munition qui correspond à leurs couleurs afin qu'ils s'activent. Par exemple, un bouton vert ne peut être activé que par la munition verte. Une fois le bouton activé, la porte qui lui est associée s'ouvre et permet au joueur de passer. La porte tant qu'a elle bloque le passage du joueur tant qu'elle n'est pas ouverte, elle ne réagit pas aux projectiles et ne s'ouvre seulement après l'activation du bouton auquel elle est associée.

![Image porte fermée](.\LOG725-tp1\docs\porte_ferme.png)

<p align="center"><em>Figure 1 : Porte fermée avant activation du bouton</em></p>

![Image porte ouverte](.\LOG725-tp1\docs\porte_ouverte.png)

<p align="center"><em>Figure 2 : Porte ouverte après activation du bouton</em></p>