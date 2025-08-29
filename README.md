## Bike Purchase Chatbot (Python CLI)

### Setup

1. Create a virtual environment (recommended):
```
python -m venv .venv
.venv\\Scripts\\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```
setx OPENAI_API_KEY "YOUR_KEY_HERE"
```
Reopen the terminal after using `setx`, or export in-session:
```
$env:OPENAI_API_KEY="YOUR_KEY_HERE"
```

Optional: choose a model (default is `gpt-4o-mini`):
```
$env:OPENAI_MODEL="gpt-4o-mini"
```

### Run

```
python main.py
```

Try messages like:
- "I commute in the city under $800"
- "gravel bike around 2500"
- "electric bike for urban rides under 3k"

If the API key is not set, the chatbot still returns local recommendations, but without LLM phrasing.

### Web App (Streamlit)

1. Install requirements (same as above) and set `OPENAI_API_KEY`.
2. Run the web app:
```
streamlit run streamlit_app.py
```
3. Open the browser URL shown by Streamlit (usually `http://localhost:8501`).

The chat panel uses OpenAI for natural language responses and the built-in catalog for recommendations. The sidebar lets you set structured preferences.


