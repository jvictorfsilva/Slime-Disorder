# Slime Disorder

**Initial Prototype TCC Project**

_Integrated Technical High School – ETEC de Hortolândia, Brazil (2022)_

---

## 📖 Overview

Slime Disorder is a 2D pixel-art RPG prototype developed during the technical high school conclusion project (TCC). Players guide a slime protagonist through the four stages of grief—Denial, Anger, Bargaining, and Acceptance—set in the fantasy realm of Sulfiria. The project demonstrates game architecture, data-driven narrative, and multimedia integration, serving as a proof-of-concept for educational and therapeutic applications.

## 🚀 Key Features

- **Four Grief Stages as Levels:** Linear progression illustrating psychological stages of mourning.
- **Interactive Narrative:** Dialogs and cutscenes loaded from CSV scripts for easy editing.
- **Entity System:** Modular classes for player, NPCs, enemies, interactive objects, and magic effects.
- **Tile-Based Maps:** Designed in Tiled (.tmx) and parsed at runtime.
- **Audio Integration:** Background music and sound effects in .ogg and .wav formats.
- **UI & HUD:** Customizable overlays for health, dialogue, and stage indicators.

## 🛠️ Technical Stack

| Component      | Technology             |
| -------------- | ---------------------- |
| Language       | Python 3.10            |
| Game Engine    | Pygame                 |
| Map Editor     | Tiled (.tmx files)     |
| Asset Creation | paint.net, Aseprite    |
| Dialog Format  | CSV (UTF-8)            |
| Audio Formats  | .ogg, .wav             |
| Dependencies   | See `requirements.txt` |

## 📁 Project Structure

```
Slime-Disorder/
├── audio/                 # Music and SFX
├── code/                  # Source code modules
│   ├── main.py            # Game entry point
│   ├── settings.py        # Configuration constants
│   ├── level.py           # Map and level logic
│   ├── entity/            # Entity module (player, NPC, enemy)
│   ├── ui/                # User interface elements
│   └── utils/             # Utilities (loader, parser, helpers)
├── dialogs/               # CSV dialog scripts per stage
├── graphics/              # Spritesheets and textures
├── map/                   # Exported CSV maps
├── requirements.txt       # Python dependencies
└── LICENSE                # MIT License
```

> _Only core directories and files shown for clarity._

## ⚙️ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/jvictorfsilva/slime-disorder.git
   cd slime-disorder
   ```

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate  # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Game

1. **Navigate to code folder**

   ```bash
   cd code
   ```

2. **Execute main script**

   ```bash
   python main.py
   ```

## 🙏 Acknowledgments

- **Sprites & Tileset** by Pixel Boy: Ninja Adventure Asset Pack ([https://pixel-boy.itch.io/ninja-adventure-asset-pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack))
- **Audio Assets** included in the same Ninja Adventure Pack by Pixel Boy

## ⚠️ Disclaimer

This is an early prototype created for an academic TCC project. It is not feature-complete and is intended for demonstration and educational purposes only.

## 📜 License

Released under the MIT License. See `LICENSE` for full terms.
