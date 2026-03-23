# ⛳ Mini Golf

A mini golf game built with Python's turtle graphics module. Click to aim and shoot your ball across 3 increasingly challenging holes, trying to finish under par!

---

## 🎮 How to Play

- **Click** anywhere on the screen to shoot the ball toward your cursor
- The further you click from the ball, the harder it hits
- Get the ball into the black hole to complete each hole
- Try to finish with as few strokes as possible
- Press **R** at any time to reset back to the main menu

---

## 🕹️ Features

- 3-hole course with increasing difficulty (Par 3 → Par 4 → Par 5)
- Running score tracker across all holes with a vs-par display
- Realistic-feeling physics with friction and energy-losing bounces
- Smart obstacle collision that detects which face was hit
- Flag marker on every hole
- Hole complete splash screen between levels
- Full win screen showing total strokes vs. par at the end
- Main menu screen before the game starts

---

## 🗺️ Holes

| Hole | Par | Description |
|------|-----|-------------|
| 1 | 3 | Gentle intro with a few scattered blocks |
| 2 | 4 | Two long walls funneling into a narrow gap, with a central pillar and near-hole blocker |
| 3 | 5 | Near maze-like layout — staggered chicane walls, island blocks, a tight corridor, and a final guard in front of the hole |

---

## 🚀 Getting Started

### Requirements

- Python 3.x (turtle is included in the standard library, no installs needed)

### Run the game

```bash
python mini_golf.py
```

---

## 🗂️ Project Structure

```
mini_golf.py   # All game code lives here
README.md
```

---

## 🛠️ Customization

How do I add my own holes? Each hole is just a dictionary in the `HOLES` list at the top of `mini_golf.py`:

```python
{
    "ball_start": (-300, 0),   # Where the ball spawns (x, y)
    "hole_pos":   (280, 0),    # Where the hole is (x, y)
    "par": 4,                  # Par for this hole
    "obstacles": [
        {"pos": (0, 0), "w": 80, "h": 40},  # (x, y), width, height
    ],
}
```

Just append a new entry to `HOLES` and the game will automatically include it!

---

## 📸 Controls Reference

| Input | Action |
|-------|--------|
| Click | Shoot ball toward cursor |
| R | Reset to main menu |
| Space | Start game from menu |
