# 8BitBarista

A Python/Pygame game project with multiple UI screens, save/load state, and minigames.

## Team

- Emrana Begum
- Arthur Zheng
- Kevin Lin
- Darren Chiu
- Jacob Szczudlik

## Run

1. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

2. Start the app:

	```bash
	python Game.py
	```

## Project Layout (high level)

- `Game.py` – login launcher / main entry point
- `first_page.py` – main in-game flow
- `screens/` – login, menu, selection, options, and other UI screen modules
- `assets/` – images, map data, sounds, sprites, buttons
- `assets/images/others/fishing/` – fishing minigame UI + sprite assets
- `data/sql/` – SQL seed/schema files
- `docs/prototypes/` – prototype/static HTML files
- `utility/` – one-off helper scripts

## Notes

- SQLite data is currently stored in `mydatabase.db`.
- Fishing minigame assets are in `assets/images/others/fishing/`.
