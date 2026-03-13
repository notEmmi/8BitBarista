# 8BitBarista
**A Retro Coffee Shop/Farming Simulator & Minigame Engine** *Built with Python, Pygame, and SQLite*



## 🚀 Overview
8BitBarista is a high-fidelity retro simulation featuring complex state management, a dynamic SQLite-backed save system, and interactive minigames. This repository represents the **Refactored Edition**, focusing on modularity, database integrity, and a professionalized asset pipeline.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Graphics:** Pygame
* **Database:** SQLite (Relational data for user states, login credentials, and inventory)
* **Design:** Figma (UI/UX Prototyping)

---

## 📅 Development Roadmap (Sprints)

### **Phase 1: Foundation & Mechanics**
* **Sprint 1: UI/UX Prototyping** – Created high-fidelity Figma prototypes for all user stories and core task flows.
* **Sprint 2: Core Infrastructure** – Implemented base features: User authentication (Login/Registration), world map, character sprites, grid-based movement, and farming mechanics.
* **Sprint 3: Systems Expansion** – Developed environmental and gameplay systems: Dynamic weather, in-game time cycles, inventory management, shop interfaces, and the fishing minigame.

### **Phase 2: Polishing & Finalization**
* **Sprint 4: Feature Completion** – Finalized semester goals:
    * UI Overhaul: Re-designed interfaces for the Shop, Fishing, and Store for better user feedback.
    * Customization: Added pet systems, house upgrades, and dynamic background music.
    * Persistence: Implemented the initial Save/Load game feature.
* **Sprint 5: Future Plans** – Improve the Save system architecture and finalize the Settings menu (Volume, Game Speed, etc.).

### **Phase 3: Independent Refactor (Personal Sprint)**
As the project transitioned from a group prototype to a portfolio-ready product, I performed a specialized **Cleanup & Quality Assurance Sprint**:
* **Repository Migration:** Deployed code to a clean repository to manage technical debt.
* **Asset Pipeline:** Organized fragmented files into a standardized directory hierarchy to fix relative pathing issues.
* **Documentation:** Authored a comprehensive README and installation guide to ensure 100% reproducibility for external developers.

---

## 🖼️ Game Gallery
| ☕ Inside the Cafe | 🌾 Farming Mechanics |
| :---: | :---: |
| ![Inside Cafe](docs/cafe.jpeg) | ![Farming](docs/farming.png) |
| *Managing NPC interactions and barista order-taking* | *Grid-based crop cultivation and tool selection system* |

| 🛒 The Shop | 🎣 Fishing Minigame |
| :---: | :---: |
| ![Store](docs/shop.png) | ![Fishing](docs/fishing.png) |
| *SQLite-driven inventory shop for items and crops* | *Timing-based reaction minigame with dynamic gold rewards* |

## 📂 Project Layout
- `Game.py` – Login launcher and main application entry point.
- `first_page.py` – Primary in-game state controller and logic flow.
- `screens/` – Modular UI components (Login, Menus, Selection, Options).
- `assets/` – Centralized images, map data, sounds, and sprites.
- `data/sql/` – SQL schema and seed files for the SQLite backend.

## ⚙️ Installation & Execution
1. **Clone & Navigate:**
   ```bash
   git clone https://github.com/notEmmi/8BitBarista
   cd 8BitBarista

2. **Install & Run:**
   ```bash
   pip install -r requirements.txt
   python Game.py
   ---
