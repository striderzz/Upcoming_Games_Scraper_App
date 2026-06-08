import os
import re
from datetime import date
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RAWG_BASE = "https://api.rawg.io/api"
API_KEY   = os.getenv("RAWG_API_KEY", "")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Each filter has: id, name, type (genre|tag), param (the actual RAWG value)
FILTERS = [
    {"id": "",               "name": "🎮 All Games",        "type": "none",  "param": ""},
    {"id": "action",         "name": "⚔️ Action",           "type": "genre", "param": "action"},
    {"id": "adventure",      "name": "🗺️ Adventure",        "type": "genre", "param": "adventure"},
    {"id": "rpg",            "name": "🧙 RPG",               "type": "genre", "param": "role-playing-games-rpg"},
    {"id": "shooter",        "name": "🔫 Shooter",           "type": "genre", "param": "shooter"},
    {"id": "fighting",       "name": "🥊 Fighting",          "type": "genre", "param": "fighting"},
    {"id": "strategy",       "name": "♟️ Strategy",          "type": "genre", "param": "strategy"},
    {"id": "simulation",     "name": "🛠️ Simulation",       "type": "genre", "param": "simulation"},
    {"id": "sports",         "name": "⚽ Sports",            "type": "genre", "param": "sports"},
    {"id": "racing",         "name": "🏎️ Racing",            "type": "genre", "param": "racing"},
    {"id": "puzzle",         "name": "🧩 Puzzle",            "type": "genre", "param": "puzzle"},
    {"id": "platformer",     "name": "🏃 Platformer",        "type": "genre", "param": "platformer"},
    {"id": "horror",         "name": "👻 Horror",            "type": "tag",   "param": "horror"},
    {"id": "survival-horror","name": "🧟 Survival Horror",   "type": "tag",   "param": "survival-horror"},
    {"id": "open-world",     "name": "🌍 Open World",        "type": "tag",   "param": "open-world"},
    {"id": "stealth",        "name": "🕵️ Stealth",          "type": "tag",   "param": "stealth"},
    {"id": "souls-like",     "name": "💀 Souls-like",        "type": "tag",   "param": "souls-like"},
    {"id": "battle-royale",  "name": "🪂 Battle Royale",     "type": "tag",   "param": "battle-royale"},
]

FILTER_MAP = {f["id"]: f for f in FILTERS}


# ── YouTube trailer lookup ─────────────────────────────────────────────────────

def get_youtube_video_id(query: str) -> str | None:
    try:
        r = requests.get(
            "https://www.youtube.com/results",
            params={"search_query": query},
            headers=HEADERS, timeout=8,
        )
        ids = re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', r.text)
        seen, unique = set(), []
        for vid in ids:
            if vid not in seen:
                seen.add(vid)
                unique.append(vid)
        return unique[0] if unique else None
    except Exception as e:
        print(f"YouTube scrape error: {e}")
        return None


# ── RAWG helpers ───────────────────────────────────────────────────────────────

def _shape(g: dict) -> dict:
    return {
        "id":           g["id"],
        "name":         g["name"],
        "release_date": g.get("released") or "TBA",
        "poster":       g.get("background_image") or "",
        "genres":       [gn["name"] for gn in g.get("genres", [])],
        "platforms":    [p["platform"]["name"] for p in (g.get("platforms") or [])][:4],
        "rating":       g.get("rating") or 0,
        "metacritic":   g.get("metacritic"),
        "slug":         g.get("slug", ""),
        "added":        g.get("added") or 0,
        "trailer":      None,
    }


def fetch_upcoming_games(filter_id: str = "", count: int = 30) -> list[dict]:
    """Fetch strictly upcoming (unreleased) games, sorted by release date."""
    today  = date.today().isoformat()
    future = "2029-12-31"

    params = {
        "key":               API_KEY,
        "dates":             f"{today},{future}",
        "ordering":          "released",
        "page_size":         40,
        "exclude_additions": True,
    }

    flt = FILTER_MAP.get(filter_id, {})
    if flt.get("type") == "genre":
        params["genres"] = flt["param"]
    elif flt.get("type") == "tag":
        params["tags"] = flt["param"]

    games, page = [], 1
    while len(games) < count:
        params["page"] = page
        try:
            r = requests.get(f"{RAWG_BASE}/games", params=params, timeout=12)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"RAWG fetch error: {e}")
            break

        results = data.get("results", [])
        if not results:
            break
        for g in results:
            if len(games) >= count:
                break
            games.append(_shape(g))

        if not data.get("next"):
            break
        page += 1

    return games


def fetch_most_awaited(count: int = 30) -> list[dict]:
    """Top awaited = upcoming games sorted by number of users who added them."""
    today  = date.today().isoformat()
    future = "2029-12-31"

    params = {
        "key":               API_KEY,
        "dates":             f"{today},{future}",
        "ordering":          "-added",         # most wishlisted / added first
        "page_size":         40,
        "exclude_additions": True,
    }

    games, page = [], 1
    while len(games) < count:
        params["page"] = page
        try:
            r = requests.get(f"{RAWG_BASE}/games", params=params, timeout=12)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"RAWG awaited error: {e}")
            break

        results = data.get("results", [])
        if not results:
            break
        for g in results:
            if len(games) >= count:
                break
            games.append(_shape(g))

        if not data.get("next"):
            break
        page += 1

    return games


def search_upcoming_games(query: str, count: int = 20) -> list[dict]:
    """Search RAWG — only upcoming/unreleased games."""
    today  = date.today().isoformat()
    future = "2029-12-31"

    params = {
        "key":       API_KEY,
        "search":    query,
        "dates":     f"{today},{future}",   # upcoming only
        "page_size": count,
        "ordering":  "-relevance",
    }
    try:
        r = requests.get(f"{RAWG_BASE}/games", params=params, timeout=10)
        r.raise_for_status()
        results = [_shape(g) for g in r.json().get("results", [])]
        return results
    except Exception as e:
        print(f"RAWG search error: {e}")
        return []


def get_similar_upcoming(game_id: int, genres: list, count: int = 10) -> list[dict]:
    """Find upcoming games with the same genres (similar recommendations)."""
    today  = date.today().isoformat()
    future = "2029-12-31"

    # Try game-series first
    results = []
    for endpoint in ("game-series", "suggested"):
        try:
            r = requests.get(
                f"{RAWG_BASE}/games/{game_id}/{endpoint}",
                params={"key": API_KEY, "page_size": 20},
                timeout=8,
            )
            r.raise_for_status()
            for g in r.json().get("results", []):
                rd = g.get("released") or ""
                if rd >= today or not rd:   # keep upcoming ones
                    results.append(_shape(g))
        except Exception:
            pass

    # If not enough, fall back to genre-based upcoming games
    if len(results) < 5 and genres:
        genre_slug = genres[0].lower().replace(" ", "-").replace("&", "and")
        try:
            r = requests.get(
                f"{RAWG_BASE}/games",
                params={
                    "key": API_KEY,
                    "dates": f"{today},{future}",
                    "genres": genre_slug,
                    "ordering": "-added",
                    "page_size": 20,
                    "exclude_additions": True,
                },
                timeout=8,
            )
            r.raise_for_status()
            for g in r.json().get("results", []):
                if g["id"] != game_id:
                    results.append(_shape(g))
        except Exception:
            pass

    seen, unique = set(), []
    for g in results:
        if g["id"] not in seen:
            seen.add(g["id"])
            unique.append(g)
    return unique[:count]


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    active = request.args.get("filter", "")
    view   = request.args.get("view", "upcoming")   # upcoming | awaited

    if view == "awaited":
        games = fetch_most_awaited(count=30)
    else:
        games = fetch_upcoming_games(filter_id=active, count=30)

    return render_template(
        "index.html",
        games=games,
        filters=FILTERS,
        active_filter=active,
        active_view=view,
    )


@app.route("/api/trailer/<int:game_id>")
def trailer_api(game_id: int):
    name = request.args.get("name", "")

    # 1. Try RAWG native clips
    try:
        r = requests.get(
            f"{RAWG_BASE}/games/{game_id}/movies",
            params={"key": API_KEY}, timeout=6,
        )
        movies = r.json().get("results", [])
        if movies:
            clip_url = (movies[0].get("data") or {}).get("480") or \
                       (movies[0].get("data") or {}).get("max")
            if clip_url:
                return jsonify({"type": "direct", "url": clip_url})
    except Exception:
        pass

    # 2. YouTube scrape
    query  = f"{name} official game trailer 2025 2026" if name else f"game {game_id} trailer"
    vid_id = get_youtube_video_id(query)
    if vid_id:
        return jsonify({"type": "youtube", "videoId": vid_id})

    return jsonify({"type": "none"})


@app.route("/api/search")
def search_api():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": [], "similar": []})

    results = search_upcoming_games(query, count=20)

    similar = []
    if results:
        top = results[0]
        similar = get_similar_upcoming(top["id"], top["genres"], count=12)

    return jsonify({"results": results, "similar": similar, "top_name": results[0]["name"] if results else ""})


if __name__ == "__main__":
    app.run(debug=True)
