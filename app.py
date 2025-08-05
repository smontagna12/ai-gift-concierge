"""Entry point for the AI‑Gift Concierge web application.

This simple Flask app serves a single page where users can input an
occasion, budget and interests to receive tailored gift suggestions.
Suggestions are generated via the OpenAI API if an API key is
available.  Otherwise a fallback list of static suggestions is
returned.  All responses are delivered as JSON for easy consumption by
the front‑end.

To run locally:

    $ export OPENAI_API_KEY=sk-...
    $ python app.py

Visit http://localhost:5000 in your browser.

"""

from __future__ import annotations

import json
import os
from typing import List, Dict

from flask import Flask, render_template, request, jsonify

try:
    # Import optional dependencies lazily.  If they aren't available
    # the app will still work using the static fallback suggestions.
    from dotenv import load_dotenv  # type: ignore
    import openai  # type: ignore
    load_dotenv()  # Load .env if present
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except Exception:
    # If import fails (e.g. no openai installed) we set variables to None
    openai = None  # type: ignore
    OPENAI_API_KEY = None


app = Flask(__name__)


def fallback_suggestions() -> List[Dict[str, str]]:
    """Return a static list of example gift ideas.

    These suggestions are used when the OpenAI API is unavailable.
    """
    return [
        {
            "name": "Aromatherapie-Duftkerzen-Set",
            "description": "Ein Set beruhigender Duftkerzen, ideal zur Entspannung.",
            "search_term": "Aromatherapie Duftkerzen Set"
        },
        {
            "name": "Kabellose Bluetooth-Kopfhörer",
            "description": "Komfortable Kopfhörer mit langer Akkulaufzeit und sattem Sound.",
            "search_term": "Kabellose Bluetooth Kopfhörer"
        },
        {
            "name": "Personalisierte Fototasse",
            "description": "Eine Tasse mit individuellem Foto – perfektes Geschenk für jeden Anlass.",
            "search_term": "Personalisierte Fototasse"
        },
    ]


def generate_gift_suggestions(occasion: str, budget: str, interests: str) -> List[Dict[str, str]]:
    """Generate gift suggestions using OpenAI's chat model.

    Args:
        occasion: The occasion for the gift (e.g. Birthday, Anniversary).
        budget: The user's budget, supplied as a string.
        interests: A description of the recipient's interests.

    Returns:
        A list of dictionaries with keys: name, description, search_term.
    """
    # If we don't have a valid API key or the openai module isn't available,
    # return the static fallback suggestions.
    if not OPENAI_API_KEY or openai is None:
        return fallback_suggestions()

    system_prompt = (
        "Du bist ein hilfsbereiter Geschenkberater. "
        "Basierend auf Anlass, Budget und Interessen des Beschenkten lieferst "
        "du eine Liste mit drei Geschenkvorschlägen. Jeder Vorschlag soll "
        "einen klaren Namen (1–5 Wörter), eine kurze Beschreibung und einen "
        "Suchbegriff enthalten, den man für eine Produktsuche verwenden kann. "
        "Verwende keine Bullet-Points oder Aufzählungszeichen; liefere "
        "stattdessen eine JSON-Liste von Objekten mit den Feldern 'name', "
        "'description' und 'search_term'."
    )
    user_prompt = (
        f"Anlass: {occasion}\n"
        f"Budget: {budget}\n"
        f"Interessen: {interests}\n"
        "Erstelle drei passende Geschenkvorschläge."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        content = response.choices[0].message["content"]
        # Attempt to parse JSON from the model output.  The model is
        # instructed to return a JSON list but we handle errors gracefully.
        suggestions = json.loads(content)
        # Validate structure: ensure each suggestion contains required keys.
        valid = []
        for item in suggestions:
            if all(k in item for k in ("name", "description", "search_term")):
                valid.append({
                    "name": item["name"],
                    "description": item["description"],
                    "search_term": item["search_term"]
                })
        if valid:
            return valid
    except Exception:
        # On any error (API error, parse error) fall back to static suggestions.
        pass
    return fallback_suggestions()


@app.route("/")
def index() -> str:
    """Render the main page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate() -> Dict[str, List[Dict[str, str]]]:
    """Handle AJAX requests to generate gift suggestions.

    Expects JSON with 'occasion', 'budget' and 'interests'.  Returns a
    JSON list of suggestions.
    """
    data = request.get_json() or {}
    occasion = data.get("occasion", "").strip()
    budget = data.get("budget", "").strip()
    interests = data.get("interests", "").strip()
    suggestions = generate_gift_suggestions(occasion, budget, interests)
    return jsonify({"suggestions": suggestions})


if __name__ == "__main__":
    # When running on a platform like Render or other PaaS providers,
    # the application needs to listen on the host 0.0.0.0 and the port
    # specified in the PORT environment variable.  Falling back to
    # 5000 ensures the app still works locally if PORT is not set.
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 5000))
    # Disable Flask's debug mode in production to avoid exposing
    # sensitive information.  Locally, you can enable debug by
    # exporting FLASK_DEBUG=1 before running the app.
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug_mode)