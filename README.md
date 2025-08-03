# Fruit Ninja Clone with Pygame

A classic fruit-slicing arcade game built with Python and the Pygame library. The objective is to slice as many fruits as you can, avoid the bombs, and achieve the highest score before time runs out or you run out of lives.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
- [How to Play](#how-to-play)
- [Code Overview](#code-overview)
- [Built With](#built-with)

## Features

- **Classic Slicing Mechanic:** Use your mouse as a blade to slice through fruits that are tossed on screen.
- **Variety of Fruits & Obstacles:** The game features multiple fruit types (Apples, Bananas, Coconuts, etc.) and game-ending bombs.
- **Scoring System:** Gain points for every fruit successfully sliced.
- **Life System:** Players start with 7 lives. A life is lost for every swipe that doesn't hit a fruit.
- **Timed Gameplay:** Each round is 60 seconds long, adding a time-pressure challenge.
- **Game Over and Restart:** A "Game Over" screen displays your final score with an option to quickly restart a new game.
- **Visual & Audio Feedback:** Includes sliced fruit animations, splash effects, and sound effects for an engaging experience.

## Getting Started

Follow these instructions to get a local copy of the game up and running on your machine.

### Prerequisites

You must have Python and the Pygame library installed.

- **Python 3.x**
- **Pygame**
  - You can install Pygame using pip:
    ```sh
    pip install pygame
    ```

### Project Structure

For the game to run correctly, your project must have the following folder and file structure. The script looks for assets in very specific paths.

```
your-project-folder/
├── fruit_ninja.py
├── assets/
│   ├── background.jpg
│   ├── apple_small.png
│   ├── banana.png
│   └── (all other fruit and effect .png files...)
└── Mobile - Fruit Ninja - Sound Effects/
└── Sound/
├── combo-1.wav
└── pome-burst.wav
```

### Installation

1.  **Download the script:**
    Save the `fruit_ninja.py` file to your project folder.

2.  **Create the Asset Folders:**
    - In the same directory as `fruit_ninja.py`, create a folder named `assets`.
    - In the same directory, create a folder named `Mobile - Fruit Ninja - Sound Effects`, and inside it, create another folder named `Sound`.

3.  **Add Game Assets:**
    - Place all the required image files (fruits, bombs, splashes, background) into the `assets` folder.
    - Place the two sound files (`combo-1.wav` and `pome-burst.wav`) into the `Mobile - Fruit Ninja - Sound Effects/Sound/` folder.

    *Note: The game includes error handling and will run without the assets, but for the full experience, these files are required.*

## How to Play

1.  **Run the Script:**
    Navigate to your project directory in your terminal and run the game using Python.
    ```sh
    python fruit_ninja.py
    ```
2.  **Gameplay:**
    - A game window will open, and fruits and bombs will start being tossed up from the bottom of the screen.
    - Move your mouse cursor across the fruits to "slice" them. The cursor is represented by a knife.
    - Slicing a fruit will increase your score by 1.
    - Slicing a bomb will instantly end the game.
    - If you move the mouse and do not slice a fruit, you will lose one life.

3.  **Game Over:**
    - The game ends when the timer reaches zero, you run out of lives, or you hit a bomb.
    - On the "Game Over" screen, press the **SPACE** key to restart the game or the **ESCAPE** key to quit.

## Code Overview

- **Initialization:** Sets up the Pygame window, loads all images and sounds with error handling, and initializes game variables.
- **`Object` Class:** A parent class for both fruits and bombs, handling their movement, gravity, and on-screen rendering.
- **`SlicedFruit` Class:** Manages the animation of a fruit being split into two halves after being sliced, including a splash effect.
- **Game Loop:** The main loop handles user input, updates the position of all objects, checks for collisions between the knife and objects, and renders everything to the screen.
- **State Management:** Functions like `reset_game()` and `show_game_over()` handle the transitions between playing and game-over states.

## Built With

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)
