# 🎮 games_scraper

A Flask web app that scrapes and displays the **Top 30 upcoming AAA games** using the [RAWG Video Games Database API](https://rawg.io/apidocs). Each game shows a poster, release date, genre tags, platform info, Metacritic score, and an in-app trailer player powered by YouTube.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![RAWG](https://img.shields.io/badge/Data-RAWG%20API-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🗓️ **Top 30 Upcoming Games** — sorted by nearest release date
- 🔥 **Top 30 Most Awaited** — sorted by how many users wishlisted the game
- 🎭 **18 Genre / Tag Filters** — Action, RPG, Horror, Survival Horror, Open World, Fighting, Souls-like, Battle Royale, and more
- 🎬 **In-app Trailer Player** — scrapes YouTube for real video IDs, plays inside a modal
- 🔍 **Search + Similar Games** — search upcoming games by name, get similar recommendations instantly
- 🌙 / ☀️ **Dark & Light Theme Toggle** — preference saved in localStorage
- 📱 **Fully Responsive** — works on desktop, tablet, and mobile

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/striderzz/game_scraper.git
cd game_scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free RAWG API key

1. Go to [https://rawg.io/apidocs](https://rawg.io/apidocs)
2. Sign up for a free account
3. Copy your API key

### 4. Configure your API key

Create a `.env` file in the project root:

```env
RAWG_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
game_scraper/
├── app.py               # Flask backend — API calls, YouTube scraping, routes
├── requirements.txt     # Python dependencies
├── .env                 # API key (not committed)
├── .gitignore
└── templates/
    └── index.html       # Frontend — dark/light UI, grid, modal, search
```

---

## 🔧 How It Works

| Feature | How |
|---|---|
| Game data | RAWG `/games` API with `dates=today,2029-12-31` |
| Most Awaited | RAWG sorted by `-added` (most wishlisted) |
| Genre filters | RAWG `genres=` param for standard genres, `tags=` for Horror / Open World etc. |
| Trailers | RAWG `/movies` endpoint first, then YouTube search scrape fallback |
| Search | RAWG `search=` + date filter → upcoming only |
| Similar games | RAWG `game-series` + `suggested` endpoints, genre fallback |

---

## 📦 Dependencies

```
flask
requests
python-dotenv
```

---

## 🌐 Genres Available

`Action` · `Adventure` · `RPG` · `Shooter` · `Fighting` · `Strategy` · `Simulation` · `Sports` · `Racing` · `Puzzle` · `Platformer` · `👻 Horror` · `🧟 Survival Horror` · `🌍 Open World` · `🕵️ Stealth` · `💀 Souls-like` · `🪂 Battle Royale`

---

## 📄 License

MIT © [striderzz](https://github.com/striderzz)
