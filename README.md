# E Card Game

A modern, Kaiji-inspired Emperor-Slave card game for Windows, featuring:

-   Beautiful Tkinter GUI with card images and animations
-   Sound effects and theme music (with volume controls)
-   Scoreboard, history, and role selection
-   One-click EXE for easy play (no Python required)

## How to Play

-   Choose your role: Emperor or Slave
-   Each round, select a card to play against the CPU
-   The rules:
    -   Emperor beats Citizen
    -   Citizen beats Slave
    -   Slave beats Emperor
    -   Same card = Draw
-   The game ends when all cards are used. The winner is determined by the last round if not a draw.

## Features

-   Modern, casino-inspired UI
-   Card flip animations
-   Sound panel for music/effects volume
-   Custom icon and standalone EXE

## Running from Source

1. Install Python 3.11+ and pip.
2. Install dependencies:
    ```
    pip install pillow pygame
    ```
3. Run the game:
    ```
    python ecarddemo.py
    ```

## Running the EXE

-   Go to the `dist` folder and double-click `E Card.exe`.
-   No Python installation required.

## Assets

-   Card images and sounds are included in the EXE.
-   Icon: `icon.ico`
-   Theme and sound effects: see project files (replace with your own if desired)

## Credits

-   Developed by [IArshia]
-   Card game inspired by Kaiji (E-Card)
-   Sound effects and images: see asset sources or replace with your own

Enjoy the game!
