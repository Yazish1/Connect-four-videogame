# Connect-four-videogame
A custom built connect-four game with additional features like Bomb and Teleport pieces, all playable directly in the command line terminal.
## Features
- Classic connect four game
- Bomb pieces - explode and clear surroudning slots
- Teleport pieces - move mirrored pieces across the board
- Gravity decorators - pieces fall naturally after explosions or teleports
- Only text-based interface
- Adjustable board size

## How to run
Usage:
python connect_four.py <rows> <columns>
Example: python connect_four.py 7 6 {creates a 7x6 connect four game}

## Gameplay
1. Players enter their username (one word) and symbol (O or X).
2. Take turns choosing which piece to play and column to drop it in. Example: X 1
3. Bomb(B) clears out surrounding slots in 3x3 grid
4. Teleport(T) pieces mirror and move another piece across the board.
5. First to connect 4 in a row (Vertically, Diagonally, Horizontally) wins.

## Created by
Yazish
