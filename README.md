# Tile Shift

A tile-sliding arcade game built with Python and Pygame. Control a blank space on a 5×5 grid to dodge and destroy enemy tiles before they overrun the board.

## Overview

Tile Shift is a 2D arcade game where the player controls a blank tile on a 5×5 grid. Slide the blank space using the arrow keys, then snap to a new position with spacebar to eliminate enemy tiles. Enemies spawn at increasing rates across multiple levels — survive as long as possible, beat your high score, and restart for another run.

## Features

* 5×5 sliding tile grid with smooth animation
* Player tile with directional movement (arrow keys)
* Attack mechanic via spacebar (snap to last moved tile)
* Enemy spawning with escalating difficulty
* Live score tracking
* level system - enemies speed up as your score grows
* Loss condition - game ends when 13 or more enemies occupy the board
* High Score Tracker - saved locally and displayed on the game over screen
* Restart from the game over screen without relaunching the game
* Title screen with animated intro and credits

## How to Play

| Control      | Action                           |
|-------------|----------------------------------|
| Arrow keys  | Slide the blank space            |
| Spacebar    | Attack — become the last tile moved |
| Enter       | Start game/Restart after game over |

Destroy red enemy tiles to earn points. The blank space fills in behind you as you move. The game ends when enemies fill 13 or more tiles - don't let them overrun the board.

## Architecture

### Tech Stack

| Layer     | Technology            |
|-----------|----------------------|
| Language  | Python 3.x            |
| Graphics  | Pygame                |
| Platform  | Desktop (cross-platform) |

### System Design

The game is structured around two core classes:
 
**Tile** - represents a single cell on the grid
```
hitbox    pygame.Rect - pixel position and size
x         int - grid column (1–5)
y         int - grid row (1–5)
container str - one of: blank | player | enemy
```
 
**Slide** - manages the screen transition animation
```
coord_1/2/3   [x, y] - three vertices of a polygon
move(amount)  shifts all vertices by a given amount
```

Key modules:
* **Tile generation** — builds the 5×5 grid at startup, removes the center tile to create the blank space
* **tile_update()** — renders all tiles each frame based on their current state
* **Input handler** — moves the blank space and resolves player/enemy collisions on spacebar
* **Enemy spawner** — timer-based system that places enemies at random tiles, with spawn rate increasing over time and capped by a minimum interval per level
* **Level System** — tracks score thresholds and reduces the enemy spawn floor on each level up
* **Loss Detection** — checks enemy count each frame and triggers game over at 13 enemies
* **High Score Tracker** — reads and writes to `highscore.txt` on disk, updates when the current score exceeds the stored value. Initializes `highscore.txt` with initial value 0 if file does not exist
* **Screen Transitions** — polygon-based wipe animation used between tile, game, and game over screens
* **wait_screen()** — renders the animated title screen and waits for Enter key to start game

## Diagrams

### Use Case Diagram

![Use Case Diagram](./diagrams/UseCaseDiagram.png)

### Class Diagram

![Class Diagram](./diagrams/ClassDiagram.png)

### Communication Diagram

![Communication Diagram](./diagrams/CommunicationDiagram.png)

## Setup & Installation

### Option 1 — Run the executable

### Option 2 — Run from source

Clone the repository
```bash
git clone https://github.com/Z-Bauer/Tiles-Project
cd Tiles-Project
```

Install dependencies
```bash
pip install pygame
```
Run the game
```bash
python Tiles-Test.py
```

## Project Status

All Sprints have been completed. See our [JIRA board](https://cis-project-350-tiles-table.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog?atlOrigin=eyJpIjoiNzAyODU1NTE3OGRlNGNiYzhlODg4ODA0N2UzZjAwNGEiLCJwIjoiaiJ9) for backlog.

## Team

| Name |
|------|
| Zach Bauer |
| Sam Sikorski |
| William Wen |
