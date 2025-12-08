<h1 align="center">🔲 ZooRush 🔳</h1>
<div id="1"></div>
</p>
<p align="center"> 
  <a href="https://github.com/deltahmed/ZooRush">
    <img src="https://img.shields.io/github/contributors/deltahmed/ZooRush.svg?style=for-the-badge" alt="deltahmed" /> </a>
  <a href="https://github.com/deltahmed/ZooRush">
    <img alt="" src="https://img.shields.io/github/issues/deltahmed/ZooRush.svg?style=for-the-badge">
    </a>
  <a href="https://github.com/deltahmed/ZooRush">
    <img alt="" src="https://img.shields.io/github/forks/deltahmed/ZooRush.svg?style=for-the-badge"></a>
  <a href="https://github.com/deltahmed/ZooRush">
    <img alt="" src="https://img.shields.io/github/stars/deltahmed/ZooRush.svg?style=for-the-badge"></a>
  <a href="https://raw.githubusercontent.com/deltahmed/ZooRush/master/LICENSE">
    <img src="https://img.shields.io/badge/License-BSD%202%20-blue?style=for-the-badge" alt="deltahmed" /> </a>
</p>

<p align="center">
  <em>A 2D farm simulation game where you build and manage your own zoo!</em>
</p>

## Language

* [English](#1)
* [Français](#2)

---

## Table of Contents

* [About The Project](#about-the-project)
* [Features](#features)
* [Installation](#installation)
* [How to Play](#how-to-play)
* [Game Controls](#game-controls)
* [Built With](#built-with)
* [Project Structure](#project-structure)
* [License](#license)
* [Credits](#credits)

---

## About The Project

**ZooRush** is a 2D farm and zoo management simulation game built with Pygame. Create your dream farm by placing enclosures, raising animals, and decorating your land with various props. Watch your farm generate income as your animals grow and thrive!

The game features:
- 🏞️ Beautiful parallax backgrounds
- 🐑 Multiple animal species (sheep, roosters, bulls, turkeys, and more)
- 🏗️ Construction system with enclosures and decorative props
- 💰 Economic system with income generation
- 🎨 Custom sprite animations
- 📷 Smooth camera controls

## Features

### 🐾 Animal Management
- **8 Different Animals**: Sheep, Rooster, Bull, Calf, Turkey, Chick, Lamb, and Piglet
- Each animal generates passive income
- Animated sprites with walking and idle states
- Animals roam freely within their enclosures

### 🏗️ Building System
- **30+ Decorative Props**: Trees, buildings, flags, bridges, and more
- **Custom Enclosures**: Build fenced areas for your animals
- **Bulldozer Mode**: Remove unwanted structures
- Income-generating buildings (houses, windmills, castles)

### 💰 Economy
- Starting capital: $2000
- Purchase animals and props
- Passive income generation from animals and buildings
- Strategic resource management

### 🎮 Gameplay Modes
- **Construction Mode**: Place enclosures and props
- **Placement Mode**: Add animals to your farm
- **Destruction Mode**: Remove structures with the bulldozer
- **Info Mode**: View detailed information about game elements

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/deltahmed/ZooRush.git
cd ZooRush
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the game**
```bash
python3 main.py
```

## How to Play

1. **Start Menu**: Launch the game and click "Play" to begin
2. **Shop Mode**: Click the shop button to browse animals and props
3. **Build Enclosures**: Select an enclosure design and place it on the map
4. **Add Animals**: Purchase animals from the shop and place them in enclosures
5. **Decorate**: Add props to beautify your farm and increase income
6. **Earn Money**: Watch as your animals and buildings generate passive income
7. **Expand**: Use your earnings to buy more animals and decorations

### Tips
- Start with cheaper animals like chickens and turkeys
- Build income-generating props like houses and windmills
- Use the info button (i) to see prices and income rates
- Plan your layout carefully - bulldozing costs money!

## Game Controls

| Control | Action |
|---------|--------|
| **Arrow Keys / WASD** | Move camera |
| **Mouse Click** | Select and place items |
| **ESC** | Pause menu |
| **Shop Button** | Open shop interface |
| **Info Button (i)** | View item information |
| **Bulldozer Button** | Enter destruction mode |

## Built With

![Python](https://img.shields.io/badge/-Python-05122A?style=for-the-badge&logo=Python)
![Pygame](https://img.shields.io/badge/-Pygame-05122A?style=for-the-badge&logo=Python)

**Technologies:**
- **Python 3.12+**: Core programming language
- **Pygame 2.6.0+**: Game development framework
- **Object-Oriented Design**: Modular architecture

## Project Structure

```
ZooRush/
├── main.py              # Game entry point and main loop
├── config.py            # Game configuration and constants
├── camera.py            # Camera system and movement
├── enclosure.py         # Enclosure and animal management
├── hud.py               # User interface and HUD elements
├── map.py               # Map rendering and tile system
├── menu.py              # Menu system
├── player.py            # Player input handling
├── render.py            # Rendering engine
├── utils.py             # Utility functions and classes
├── requirements.txt     # Python dependencies
└── media/               # Game assets
    ├── animals/         # Animal sprites
    ├── hud/             # UI elements
    ├── parallax/        # Background layers
    ├── props/           # Decorative objects
    └── tiles/           # Ground tiles
```

## License

![Licence](https://img.shields.io/badge/License-BSD%202%20-blue?style=for-the-badge)

Distributed under the BSD 2-Clause License. See `LICENCE.txt` for more information.

## Credits

### Assets
- **Animals & Props**: [CraftPix.net](https://craftpix.net/) - See `media/licences/craftpix License.txt`
- **Parallax Backgrounds**: Raventale (itch.io) - See `media/licences/Raventale itch.io Licence`
- **Font**: Soup of Justice - See `media/licences/Soup of Justice License.txt`

### Development

<a href="https://github.com/deltahmed/Click-journeY/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=deltahmed/ZooRush" />
</a>


![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)
![Img](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)

<div id="2"></div>
<h1 align="center">🔲 ZooRush - Français 🔳</h1>
<div id="1"></div>
</p>
<p align="center"> 
  <a href="https://github.com/deltahmed/ZooRush">
    <img src="https://img.shields.io/github/contributors/deltahmed/ZooRush.svg?style=for-the-badge" alt="deltahmed" /> </a>
  <a href="https://github.com/deltahmed/ZooRush">
    <img alt="" src="https://img.shields.io/github/issues/deltahmed/ZooRush.svg?style=for-the-badge">
    </a>
  <a href="https://github.com/deltahmed/ZooRush">
    <img alt="" src="https://img.shields.io/github/forks/deltahmed/ZooRush.svg?style=for-the-badge"></a>
  <a href="https://github.com/deltahmed/ZooRush">
    <img alt="" src="https://img.shields.io/github/stars/deltahmed/ZooRush.svg?style=for-the-badge"></a>
  <a href="https://raw.githubusercontent.com/deltahmed/ZooRush/master/LICENSE">
    <img src="https://img.shields.io/badge/License-BSD%202%20-blue?style=for-the-badge" alt="deltahmed" /> </a>
</p>

<p align="center">
  <em>Un jeu de simulation de ferme 2D où vous construisez et gérez votre propre zoo !</em>
</p>

## Langue

* [English](#1)
* [Français](#2)

---

## Table des Matières

* [À propos du projet](#à-propos-du-projet)
* [Fonctionnalités](#fonctionnalités)
* [Installation](#installation-fr)
* [Comment jouer](#comment-jouer)
* [Contrôles du jeu](#contrôles-du-jeu)
* [Conçu avec](#conçu-avec)
* [Structure du projet](#structure-du-projet)
* [Licence](#licence-fr)
* [Crédits](#crédits)

---

## À propos du projet

**ZooRush** est un jeu de simulation de gestion de ferme et de zoo en 2D développé avec Pygame. Créez la ferme de vos rêves en plaçant des enclos, en élevant des animaux et en décorant vos terres avec divers accessoires. Regardez votre ferme générer des revenus au fur et à mesure que vos animaux grandissent et prospèrent !

Le jeu propose :
- 🏞️ De magnifiques arrière-plans en parallaxe
- 🐑 Plusieurs espèces d'animaux (moutons, coqs, taureaux, dindes, et plus)
- 🏗️ Système de construction avec enclos et accessoires décoratifs
- 💰 Système économique avec génération de revenus
- 🎨 Animations de sprites personnalisées
- 📷 Contrôles de caméra fluides

## Fonctionnalités

### 🐾 Gestion des animaux
- **8 Animaux différents** : Mouton, Coq, Taureau, Veau, Dinde, Poussin, Agneau et Porcelet
- Chaque animal génère un revenu passif
- Sprites animés avec états de marche et d'inactivité
- Les animaux se déplacent librement dans leurs enclos

### 🏗️ Système de construction
- **Plus de 30 accessoires décoratifs** : Arbres, bâtiments, drapeaux, ponts, et plus
- **Enclos personnalisés** : Construisez des zones clôturées pour vos animaux
- **Mode bulldozer** : Supprimez les structures indésirables
- Bâtiments générateurs de revenus (maisons, moulins à vent, châteaux)

### 💰 Économie
- Capital de départ : 2000 $
- Achetez des animaux et des accessoires
- Génération de revenus passifs par les animaux et les bâtiments
- Gestion stratégique des ressources

### 🎮 Modes de jeu
- **Mode construction** : Placez des enclos et des accessoires
- **Mode placement** : Ajoutez des animaux à votre ferme
- **Mode destruction** : Supprimez des structures avec le bulldozer
- **Mode info** : Consultez des informations détaillées sur les éléments du jeu

## Installation-fr

### Prérequis

- Python 3.8 ou supérieur
- pip (installateur de paquets Python)

### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/deltahmed/ZooRush.git
cd ZooRush
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer le jeu**
```bash
python3 main.py
```

## Comment jouer

1. **Menu de démarrage** : Lancez le jeu et cliquez sur "Play" pour commencer
2. **Mode boutique** : Cliquez sur le bouton boutique pour parcourir les animaux et accessoires
3. **Construire des enclos** : Sélectionnez un design d'enclos et placez-le sur la carte
4. **Ajouter des animaux** : Achetez des animaux dans la boutique et placez-les dans les enclos
5. **Décorer** : Ajoutez des accessoires pour embellir votre ferme et augmenter les revenus
6. **Gagner de l'argent** : Regardez vos animaux et bâtiments générer des revenus passifs
7. **Développer** : Utilisez vos gains pour acheter plus d'animaux et de décorations

### Conseils
- Commencez avec des animaux moins chers comme les poulets et les dindes
- Construisez des accessoires générateurs de revenus comme les maisons et les moulins à vent
- Utilisez le bouton info (i) pour voir les prix et les taux de revenus
- Planifiez votre agencement avec soin - utiliser le bulldozer coûte de l'argent !

## Contrôles du jeu

| Contrôle | Action |
|----------|--------|
| **Flèches / WASD** | Déplacer la caméra |
| **Clic souris** | Sélectionner et placer des éléments |
| **ESC** | Menu pause |
| **Bouton boutique** | Ouvrir l'interface boutique |
| **Bouton info (i)** | Voir les informations sur les éléments |
| **Bouton bulldozer** | Entrer en mode destruction |

## Conçu avec

![Python](https://img.shields.io/badge/-Python-05122A?style=for-the-badge&logo=Python)
![Pygame](https://img.shields.io/badge/-Pygame-05122A?style=for-the-badge&logo=Python)

**Technologies :**
- **Python 3.12+** : Langage de programmation principal
- **Pygame 2.6.0+** : Framework de développement de jeux
- **Conception orientée objet** : Architecture modulaire

## Structure du projet

```
ZooRush/
├── main.py              # Point d'entrée et boucle principale
├── config.py            # Configuration et constantes du jeu
├── camera.py            # Système de caméra et déplacement
├── enclosure.py         # Gestion des enclos et des animaux
├── hud.py               # Interface utilisateur et éléments HUD
├── map.py               # Rendu de la carte et système de tuiles
├── menu.py              # Système de menu
├── player.py            # Gestion des entrées joueur
├── render.py            # Moteur de rendu
├── utils.py             # Fonctions et classes utilitaires
├── requirements.txt     # Dépendances Python
└── media/               # Ressources du jeu
    ├── animals/         # Sprites d'animaux
    ├── hud/             # Éléments d'interface
    ├── parallax/        # Couches d'arrière-plan
    ├── props/           # Objets décoratifs
    └── tiles/           # Tuiles de sol
```

## Licence-fr

![Licence](https://img.shields.io/badge/License-BSD%202%20-blue?style=for-the-badge)

Distribué sous licence BSD 2-Clause. Voir `LICENCE.txt` pour plus d'informations.

## Crédits

### Ressources
- **Animaux et accessoires** : [CraftPix.net](https://craftpix.net/) - Voir `media/licences/craftpix License.txt`
- **Arrière-plans parallaxe** : Raventale (itch.io) - Voir `media/licences/Raventale itch.io Licence`
- **Police** : Soup of Justice - Voir `media/licences/Soup of Justice License.txt`

### Développement

<a href="https://github.com/deltahmed/Click-journeY/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=deltahmed/ZooRush" />
</a>

![Python](https://img.shields.io/badge/-Python-05122A?style=for-the-badge&logo=Python)

## Licence 
![Licence](https://img.shields.io/badge/License-BSD%202%20-blue?style=for-the-badge)



