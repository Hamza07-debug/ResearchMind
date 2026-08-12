# ResearchMind — Multi-Agent AI Research Pipeline

A fully autonomous multi-agent AI system that researches any topic by searching the web, scraping deep content, writing a structured report, and critically reviewing it — all in one pipeline.

Built with **LangChain**, **LangGraph**, **Mistral AI**, **Tavily Search**, and **Streamlit**.

---

## Demo

![ResearchMind Pipeline](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![LangChain](https://img.shields.io/badge/Framework-LangChain-green) ![Mistral](https://img.shields.io/badge/LLM-Mistral%20AI-orange)

---

## How It Works

ResearchMind runs four specialized AI agents in sequence:

```
Topic Input
    │
    ▼
┌─────────────────┐
│  01 Search Agent │  ── Tavily web search (last 30 days)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  02 Reader Agent │  ── Scrapes the most relevant URL for deep content
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  03 Writer Chain │  ── Synthesises a structured research report
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  04 Critic Chain │  ── Scores and reviews the report (X/10)
└─────────────────┘
         │
         ▼
  Final Report + Score
```

| Agent | Role | Tool |
|---|---|---|
| Search Agent | Finds recent web results on the topic | Tavily Search API |
| Reader Agent | Scrapes the most relevant URL for deeper content | BeautifulSoup |
| Writer Chain | Writes a structured report (Intro, Key Findings, Conclusion, Sources) | Mistral LLM |
| Critic Chain | Reviews the report and gives a score out of 10 with actionable feedback | Mistral LLM |

---

## Features

- **Real-time web search** — Tavily fetches results from the last 30 days
- **Deep content scraping** — Reader agent picks the best URL and extracts full page content
- **Token-by-token streaming** — Writer and Critic responses stream live in the UI
- **Quality scoring** — Critic agent scores every report out of 10 with strengths and improvement suggestions
- **Download reports** — Export the final report as `.txt` or `.pdf`
- **Rate limit handling** — Automatic retry with backoff on API 429 errors
- **Dark UI** — Custom-styled Streamlit interface with animated hero, pipeline cards, and live status indicators

---

## Project Structure

```
ResearchMind/
│
├── app.py              # Streamlit UI — full pipeline runner with live streaming
├── agents.py           # Agent and chain definitions (Search, Reader, Writer, Critic)
├── tools.py            # LangChain tools (web_search via Tavily, scrape_url via BS4)
├── pipeline.py         # CLI pipeline runner (terminal version, no UI)
├── requirements.txt    # All dependencies
└── .env                # API keys (not committed)
```

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/Hamza07-debug/ResearchMind.git
cd ResearchMind
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

- Get your Mistral API key at [console.mistral.ai](https://console.mistral.ai)
- Get your Tavily API key at [app.tavily.com](https://app.tavily.com)

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### 6. (Optional) Run in terminal only

```bash
python pipeline.py
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral Large (via `langchain-mistralai`) |
| Agent Framework | LangGraph `create_react_agent` |
| Web Search | Tavily Search API |
| Web Scraping | `requests` + `BeautifulSoup4` |
| UI | Streamlit |
| Rate Limiting | LangChain `InMemoryRateLimiter` |
| PDF Export | `fpdf` |

---

## Environment Variables

| Variable | Description |
|---|---|
| `MISTRAL_API_KEY` | API key for Mistral AI |
| `TAVILY_API_KEY` | API key for Tavily Search |

---

## Notes

- The pipeline uses a **0.5 requests/second rate limiter** to avoid Mistral API 429 errors. If you hit limits, the app will automatically retry with backoff.
- Tavily search is filtered to results from the **last 30 days** to ensure the report is based on recent information.
- The `.env` file is excluded from the repo via `.gitignore` — never commit your API keys.

---

## Author

**Hamza** — [github.com/Hamza07-debug](https://github.com/Hamza07-debug)
