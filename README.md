<div align="center">

# FatalCraft

**A 2D Minecraft-inspired sandbox built from scratch with Pygame**

<img src="https://skillicons.dev/icons?i=python" width="64" />&nbsp;&nbsp;<img src="https://go-skill-icons.vercel.app/api/icons?i=pygame" width="64" />

<br/>

![Status](https://img.shields.io/badge/STATUS-ACTIVE-4CAF50?style=for-the-badge&logoColor=white)
![Language](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Library](https://img.shields.io/badge/PYGAME-00B140?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/LICENSE-MIT-0078D4?style=for-the-badge&logoColor=white)

*Mining. Crafting. Mobs. Explosions. Full day/night cycle. All in 2D.*

---

</div>

## Screenshots

<div align="center">
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/92e17592-fa8e-48c5-aadc-615514669d5a" width="388" height="292" />
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/fd6af342-a793-4f82-847e-2c5b20cad6c5" width="388" height="292" />
    </td>
  </tr>
</table>
</div>

---
## Video

<div align="center">
  <table>
    <tr>
      <td align="center">
        <iframe 
          width="420" 
          height="315"
          src="https://www.youtube.com/embed/mh3TD6VMthE"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen>
        </iframe>
      </td>
    </tr>
  </table>
</div>

---
## Features

### World & Blocks

- Infinite scrolling world with chunk-based generation
- Block types: Grass, Dirt, Stone, Coal, Iron, Diamond, Bedrock
- Trees with Wood and Leaves (physics pass-through — see [Changelog](#changelog))
- Block-breaking progress bar and particle effects
- Block placing with structural support checks

### Player

- Smooth movement, sprinting (Shift), and camera tracking
- Industry-standard axis-separated collision (see [Changelog](#changelog))
- Jump, fall damage, and mining range
- Heart-based health system with custom icons
- Hotbar (9 slots) and inventory with stack counts

### Crafting System

| Feature | Details |
|---|---|
| Grid | 3×3 crafting grid |
| Toggle | `E` key |
| Recipes | Sticks, pickaxes, and more |
| Item transfer | Inventory ↔ crafting grid |

### Day / Night Cycle

- Dynamic ambient lighting tied to time of day
- Passive mobs spawn during the day, hostile mobs spawn at night

### Mobs

**Passive** — Pig, Sheep (wandering, idle, walking, knockback physics)

**Hostile** — Zombie, Spider, Creeper (full explosion system with block destruction)

---

## Controls

| Action | Key / Button |
|---|---|
| Move Left / Right | `A` / `D` |
| Jump | `W` or `Space` or `↑` |
| Break Block | Left Click |
| Place Block | Right Click |
| Open Crafting Table | `E` |
| Select Hotbar Slot | `1` – `9` |
| Previous / Next Slot | `[` / `]` |
| Sprint | Left Shift |
| Toggle Fullscreen | `F11` |

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/PrathyayPGM-ALT/Minecraft-but-2D
cd Minecraft-but-2D/Minecraft
```

**2. Install dependencies**
```bash
pip install pygame
```

**3. Run the game**
```bash
python main.py
```

> Requires Python 3.x and Pygame. No other dependencies.

---

## Project Structure

```
Minecraft-but-2D/
│
├── Minecraft/
│   ├── main.py             # Game entry point & main loop
│   ├── crafting.py         # Crafting grid logic and recipes
│   ├── launcher.py         # Launcher / menu screen
│   ├── textures/           # Block and mob sprites
│   │   ├── dirt.png
│   │   ├── stone.png
│   │   ├── stick.png
│   │   └── ...
│   └── sounds/
│       └── hurt.mp3
│
└── README.md
```

---

## Changelog

### Axis-Separated Collision (Jump / Block Fix)

`Player.update()` now uses the industry-standard two-phase collision approach:

- **Horizontal phase first** — move by `dx`, push back on wall contact (no erroneous top-snap)
- **Vertical phase second** — apply gravity, snap to block top only when falling onto it from above

Previously, a single collision pass couldn't distinguish "walking into a wall" from "landing on a floor", causing both to trigger a top-snap.

---

### Infinite World Generation

- Added `World.generated_chunk_cols` (a set) to track which 800px-wide columns have terrain
- `World.ensure_chunk_col(chunk_col_x)` generates grass, dirt, stone, ores, bedrock, and trees for any new column
- `generate_world()` now seeds ~14 chunks around spawn instead of a fixed range
- Every frame, the main loop ensures 4 chunks ahead and behind the player — new terrain loads seamlessly in both directions
- Loaded save data automatically marks its chunk columns as already generated

---

### Fullscreen Support

- `F11` toggles between fullscreen and the default 1000×800 windowed mode
- On toggle: camera viewport, hotbar, health bar, and death-screen button positions all update automatically
- `draw_hotbar` and `draw_health_bar` use `screen.get_size()` to anchor to the bottom of whatever screen size is active
- Window resizing (drag) also correctly updates the camera and UI button positions

---

### Tree Pass-Through

Added `isinstance(block, (Wood, Leaves))` checks in both collision phases:

- **Horizontal** — wood and leaves are skipped so the player walks through tree trunks without wall collision
- **Vertical** — wood and leaves are skipped so the player doesn't land on top of or get stuck inside trees

Mining and placing still work normally — only physics collision is bypassed.

---

## Roadmap

- [ ] Smelting & furnaces
- [ ] Mobs dropping items on death
- [ ] Biome variety
- [ ] Cave generation
- [ ] Polished inventory UI
- [ ] Boss mobs
- [ ] Bow & arrows
- [ ] Armour system
- [ ] Per-block sound effects
- [ ] Save / load crafting grid state

---

## Contributing

Contributions are welcome. Open a pull request or issue if you'd like to add features, fix bugs, or suggest improvements.

---

## Credits

Thanks to the Discord crew who kept this project alive:

- **Blake** (h0hx) — pls stop changing usernames
- **Craxzy** — trying to flex Nitro
- **Red code** — for the challenge and trashing Python

---

<div align="center">

If you find this project interesting, drop a star on GitHub and follow **PrathyayPGM-ALT** for more.

</div>
