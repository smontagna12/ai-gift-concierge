## AI‑Gift Concierge

This repository contains a minimal **AI‑powered gift recommender** web application.  
Users answer a few simple questions (occasion, budget and interests) and the service
returns a curated list of gift suggestions along with affiliate search phrases.

The goal of this project is to demonstrate a lean MVP that can be
extended into a fully‑fledged product.  The current implementation
relies on the OpenAI API to generate personalized recommendations,
but it also includes a fallback mode with static suggestions for
development or demo purposes.

### Features

* 🧠 **AI‑driven suggestions:** Each query is turned into a short list of
  gift ideas tailored to the recipient’s interests and budget.  The model
  produces product names, brief descriptions and search keywords that
  can be linked to affiliate programs (e.g. Amazon, eBay).
* 📄 **Simple form interface:** The front‑end is a single page that collects
  occasion, budget and interests, then displays results without reloading.
* 🔄 **API fallback:** If the OpenAI API is not configured (no
  `OPENAI_API_KEY` provided), the application returns a predefined list
  of sample suggestions so you can test the UI and workflow.

### Quick start

Clone the repository and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set the `OPENAI_API_KEY` environment variable to your OpenAI API key
(optional).  Without a key the app will fall back to static suggestions.

```bash
export OPENAI_API_KEY="sk-your-key-here"
python app.py
```

The application will start at `http://localhost:5000`.  Navigate
to the page, fill in the form and review the generated suggestions.

### Deployment

This code is intentionally minimal.  For production use you will want
to add proper error handling, rate limiting, caching and possibly
background tasks for long‑running operations.  You can deploy this app
to any platform that supports Python, such as Heroku, Render or a
container orchestrator like Docker.

### License

This project is released under the MIT License.  See the
[`LICENSE`](LICENSE) file for details.