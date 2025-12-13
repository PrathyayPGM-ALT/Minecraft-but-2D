# ⛏️ FatalCraft – A 2D Minecraft-Inspired Sandbox  
A fully custom-built 2D Minecraft clone made with **Pygame**, featuring mining, crafting, mobs, particles, day/night cycle, and more.  
Created by **PrathyayPGM-ALT** (the ultimate chaos dev).

---

## 🎮 Features

### 🧱 World & Blocks
- Infinite-style scrolling world  
- Grass, dirt, stone, coal, iron, diamond, bedrock  
- Trees with wood + leaves  
- Block breaking progress bar  
- Block placing with support checks  
- Chunk-based world system  
- Particle effects when you break blocks  

### 👤 Player
- Smooth movement & camera  
- Sprinting (Shift)  
- Jumping & fall damage  
- Hotbar (9 slots)  
- Mining range  
- Inventory with stack counts  
- Heart-based health system with custom icons  

### 🔨 Crafting System
- 3×3 crafting grid  
- Recipes (stick, pickaxes, etc.)  
- Output slot  
- Works with `E` key toggle  
- Items move between inventory ↔ crafting grid  

### 🌙 Day & Night Cycle
- Dynamic lighting  
- Daytime: passive mobs spawn  
- Nighttime: hostile mobs spawn  

### 🐾 Mobs  
#### Passive  
- 🐖 Pig  
- 🐑 Sheep  
(with wandering, idle, walking, physics, knockback)

#### Hostile  
- 🧟 Zombie  
- 🕷️ Spider  
- 💥 Creeper (full exploding system with block destruction)

---

## 🎮 Controls

| Action | Key |
|--------|-----|
| Move Left / Right | A / D |
| Jump | W / Space / ↑ |
| Break Block | Left Click |
| Place Block | Right Click |
| Open Crafting Table | E |
| Select Hotbar Slot | 1–9 |
| Previous / Next Slot | [ or ] |
| Craft Item | Mouse Click |
| Sprint | Left Shift |

---

## 📦 Installation  

### 1️⃣ Clone the repo  
```bash
git clone https://github.com/PrathyayPGM-ALT/Minecraft-but-2D
cd Minecraft-but-2D/Minecraft
```

### 2️⃣ Install dependencies  
```bash
pip install pygame
```

### 3️⃣ Run the game  
```bash
python main.py
```

---

## 🗂️ Project Structure
```
Minecraft-but-2D/
│
├── Minecraft/
│   ├── main.py
│   ├── crafting.py
│   ├── textures/
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
## Screenshots

<div align="center">

<table>
  <tr>
    <td align="center">
      <img 
        src="https://github.com/user-attachments/assets/92e17592-fa8e-48c5-aadc-615514669d5a" 
        width="388"
        height = "292"
      />
    </td>
    <td align="center">
      <img 
        src="https://github.com/user-attachments/assets/fd6af342-a793-4f82-847e-2c5b20cad6c5" 
        width="388"
        height = "292"
      />
    </td>
  </tr>
</table>

</div>

---

## 🛠️ To-Do / Future Features
- Tools (pickaxes change mining speed)  
- Smelting & furnaces  
- Mobs dropping items  
- Biomes  
- Cave generation  
- Real inventory UI  
- Boss mobs  
- Bow & arrows  
- Armor system  
- Sound effects for blocks  
- Better textures  
- Saving + loading crafting grid  

---

## 💡 Contributing  
Contributions welcome!  
Open a PR or issue if you want to add features or fix bugs.

---

## ⭐ Like the project?  
Leave a **star ⭐ on GitHub** and follow **PrathyayPGM-ALT** for more chaos-powered projects.  
