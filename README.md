# Monday.com Business Intelligence Agent

A conversational BI agent that connects to Monday.com boards and answers natural-language business questions using live data and OpenAI.

## How It Works

1. User asks a question in the Streamlit chat UI.
2. **Intent detection** classifies the query as `deals`, `work_orders`, or `cross_board` using keyword matching.
3. Relevant Monday.com boards are fetched via the GraphQL API.
4. Raw records are cleaned and normalized (currency parsing, sector title-casing).
5. Pipeline analysis runs — deal count, total value, sector breakdown, health assessment, and optionally conversion rate.
6. Results plus the user question are sent to OpenAI for an executive-level summary.
7. The answer and an action trace are displayed in the UI.

## Architecture

```
app.py  (Streamlit UI)
  └─ agent.py  (orchestration + intent detection)
       ├─ monday_api.py  (Monday.com GraphQL client)
       ├─ cleaner.py     (data normalization)
       ├─ analysis.py    (pipeline & sector metrics)
       ├─ llm.py         (OpenAI Responses API wrapper)
       └─ prompts.py     (system prompt definition)
```

## Setup

### Prerequisites

- Python 3.9+
- A Monday.com account with API access
- An OpenAI API key

### Install

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
MONDAY_API_KEY=your_monday_api_key
DEALS_BOARD=your_deals_board_id
WORK_ORDERS_BOARD=your_work_orders_board_id
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini          # optional, defaults to gpt-4.1-mini
```

### Run

```bash
streamlit run app.py
```

## Features

- **Deals analysis** — pipeline value, deal count, pipeline health, top 5 sectors.
- **Work orders analysis** — total work order count.
- **Cross-board analysis** — deals-to-work-orders conversion rate.
- **Auto-detection** — sector and money columns are detected by name heuristics, not hardcoded.
- **Agent trace** — every step (API calls, row counts, analysis phase) is logged and viewable in an expandable panel.

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| LLM | OpenAI (`gpt-4.1-mini` default, Responses API) |
| Data | Pandas |
| External API | Monday.com GraphQL API |
| Config | python-dotenv |

## Limitations

- Board queries are capped at **500 items** (no pagination).
- Intent detection is keyword-based, not LLM-driven.
- Column detection relies on name heuristics (`"sector"`, `"value"`, `"amount"` in column title).
