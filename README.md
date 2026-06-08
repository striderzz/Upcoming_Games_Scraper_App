# games_scraper

A Flask web application that fetches and displays the **Top 30 upcoming AAA games** using the [RAWG Video Games Database API](https://rawg.io/apidocs). Each game card shows a poster, release date, genre tags, platform list, Metacritic score, and an in-app trailer player backed by YouTube.

<img width="2560" height="1331" alt="Screenshot (671)" src="https://github.com/user-attachments/assets/f8eddea9-9156-4a7e-ac35-3cbdf0639490" />


---

## Features

- **Top 30 Upcoming Games** — sorted by nearest release date, strictly unreleased titles only
- **Top 30 Most Awaited** — sorted by the number of users who wishlisted the game on RAWG
- **17 Genre and Tag Filters** — Action, Adventure, RPG, Shooter, Fighting, Strategy, Simulation, Sports, Racing, Puzzle, Platformer, Horror, Survival Horror, Open World, Stealth, Souls-like, Battle Royale
- **In-App Trailer Player** — scrapes YouTube search results for a real video ID and plays it inside a modal overlay
- **Search with Similar Recommendations** — search upcoming games by name and instantly see related upcoming titles
- **Dark and Light Theme** — one-click toggle, preference stored in localStorage
- **Fully Responsive** — desktop, tablet, and mobile layouts

---

## Preview

| Top Awaited | Upcoming by Genre |
|---|---|
| ![Top Awaited](screenshots/preview.png) | Filter any genre from the nav bar |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/striderzz/game_scraper.git
cd game_scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free RAWG API key

1. Visit [https://rawg.io/apidocs](https://rawg.io/apidocs)
2. Create a free account
3. Copy your API key from the dashboard

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
RAWG_API_KEY=your_api_key_here
```

> The `.env` file is listed in `.gitignore` and will never be committed.

### 5. Run the development server

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## Project Structure

```
game_scraper/
├── app.py                  # Flask backend — RAWG API calls, YouTube scraping, routes
├── requirements.txt        # Python dependencies
├── .env                    # API key — never committed
├── .gitignore
├── screenshots/
│   └── preview.png         # App screenshot for README
└── templates/
    └── index.html          # Frontend — cards, modal, search, theme toggle
```

---

## How It Works

| Feature | Implementation |
|---|---|
| Game data | RAWG `/games` endpoint filtered to `dates=today,2029-12-31` |
| Most Awaited | Same endpoint ordered by `-added` (most wishlisted first) |
| Genre filters | `genres=` param for standard genres; `tags=` param for Horror, Open World, etc. |
| Trailers | RAWG `/movies` endpoint first; YouTube search scrape fallback |
| Search | RAWG `search=` combined with future date filter — upcoming titles only |
| Similar games | RAWG `game-series` and `suggested` endpoints, genre-based fallback |
| Theme | CSS custom properties swapped via `data-theme` attribute on `<html>` |

---

## Dependencies

```
flask
requests
python-dotenv
```

No paid services or external JavaScript frameworks required.

---

## Genre Filters

| Filter | Type | RAWG Param |
|---|---|---|
| Action | Genre | `action` |
| Adventure | Genre | `adventure` |
| RPG | Genre | `role-playing-games-rpg` |
| Shooter | Genre | `shooter` |
| Fighting | Genre | `fighting` |
| Strategy | Genre | `strategy` |
| Simulation | Genre | `simulation` |
| Sports | Genre | `sports` |
| Racing | Genre | `racing` |
| Puzzle | Genre | `puzzle` |
| Platformer | Genre | `platformer` |
| Horror | Tag | `horror` |
| Survival Horror | Tag | `survival-horror` |
| Open World | Tag | `open-world` |
| Stealth | Tag | `stealth` |
| Souls-like | Tag | `souls-like` |
| Battle Royale | Tag | `battle-royale` |

---

## License

MIT License. See [LICENSE](LICENSE) for details.
