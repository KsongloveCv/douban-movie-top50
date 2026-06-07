from flask import Flask, jsonify, render_template
from douban_crawler import DoubanTopCrawler
import json
import os

app = Flask(__name__)

DATA_FILE = "douban_top50.json"


def _load_cached_movies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _fetch_and_cache():
    crawler = DoubanTopCrawler(count=50)
    movies = crawler.crawl()
    if movies:
        crawler.save_json(movies, DATA_FILE)
    return movies


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/movies")
def api_movies():
    movies = _load_cached_movies()
    if movies is None:
        movies = _fetch_and_cache()
    if movies is None:
        return jsonify({"error": "Failed to fetch movies from Douban"}), 500
    return jsonify(movies)


@app.route("/api/refresh")
def api_refresh():
    movies = _fetch_and_cache()
    if movies is None:
        return jsonify({"error": "Failed to fetch movies from Douban"}), 500
    return jsonify({"count": len(movies), "message": "Data refreshed successfully"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)