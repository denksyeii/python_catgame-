# catgame

This is a logic grid game built in Python with Pygame, heavily inspired by puzzles like *Star Battle*. The goal is pretty straightforward: place $N$ cats on an $N \times N$ color-divided board without breaking the placement rules.

Instead of relying on hardcoded levels, the game generates a fresh board every time you run it. It uses a backtracking algorithm to secretly place the cats first—guaranteeing the puzzle is actually solvable—and then grows the colored regions around them.

---

## How to Play

To beat the level, you need to place **8 cats** on the grid while following four basic rules:

1. **One per row:** You can only have one cat in each horizontal row.
2. **One per column:** Only one cat per vertical column.
3. **One per color:** Each colored region can only hold a single cat.
4. **Personal space:** Cats cannot touch each other, not even diagonally (all 8 surrounding tiles around a cat must be free of other cats).

---

## Controls

Everything works with a single button (left-click), making it comfortable for mice, trackpads, or touchscreens:

* **Quick click:** Places or removes a cross (`X`). Useful for ruling out tiles where you know a cat can't go.
* **Click and hold (0.3 seconds):** Places or removes a cat.

If you place a cat that breaks any of the rules, the game will highlight the conflicting cats in red right away.

---

## Running the Game

You just need Python 3 and Pygame installed.

1. Clone the repo:
   ```bash
   git clone [https://github.com/your-username/your-repository.git](https://github.com/your-username/your-repository.git)
   cd your-repository
   ```
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the script:
   ```bash
   python main.py
   ```

---

## Custom Sprites



The script looks for three image files in the same directory:
* `gato_normal.png` (standard cat sprite)
* `gato_error.png` (displayed when a rule is broken)
* `equis.png` (the cross mark for ruled-out tiles)

If the images aren't there, don't worry—the game won't crash. It automatically falls back to drawing black, red, and gray squares so it stays completely playable out of the box.

---

## Quick Tweaks

If you want to make the board bigger or resize the window, just change these two constants at the very top of the script:

```python
N = 8                # Number of rows, columns, regions, and cats
TAMANO_CELDA = 70    # Pixel size for each grid tile
```

---
