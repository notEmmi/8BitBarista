# 8BitBarista
**A Retro Coffee Shop Simulator & Minigame Engine** *Built with Python, Pygame, and SQLite*

[Image of 8-bit retro game interface showing a coffee shop counter]

## 🚀 Overview
8BitBarista is a high-fidelity retro simulation featuring complex state management, a dynamic SQLite-backed save system, and interactive minigames. This repository represents a **refactored edition**, focusing on code modularity, database integrity, and an optimized asset pipeline.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Graphics:** Pygame
* **Database:** SQLite (Relational data for user states, login credentials, and inventory)
* **Architecture:** Modular Screen Pattern

## 📈 Refactoring Sprint (Feb 2026)
Following the initial prototype phase, I led a specialized cleanup sprint to move the codebase toward production standards:
* **Directory Restructuring:** Migrated loose assets into a standardized `/assets` hierarchy to resolve relative pathing issues across different OS environments.
* **Database Optimization:** Audited `data/sql/` seed files to ensure relational integrity for user save states and persistent inventory tracking.
* **Code Quality:** Refactored main entry points (`Game.py` and `first_page.py`) to reduce global variable dependency and improve memory management during screen transitions.
* **Documentation:** Authored comprehensive installation guides and detailed the project architecture for future contributors.

## 🖼️ Gallery
| Brewing Logic | Inventory Management | Fishing Minigame |
| :---: | :---: | :---: |
| ![Brewing](docs/images/brewing.png) | ![Inventory](docs/images/inventory.png) | ![Fishing](docs/images/fishing.png) |

## 📂 Project Layout
- `Game.py` – Login launcher and main application entry point.
- `first_page.py` – Primary in-game state controller and logic flow.
- `screens/` – Modular UI components (Login, Menus, Selection, Options).
- `assets/` – Centralized repository for images, map data, sounds, and sprites.
- `data/sql/` – SQL schema and seed files for the SQLite backend.
- `utility/` – Developer helper scripts for asset processing.

## ⚙️ Installation & Execution
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/8BitBarista-Refactored.git](https://github.com/YourUsername/8BitBarista-Refactored.git)
   cd 8BitBar