import os
from monday_api import fetch_board
from cleaner import clean_dataframe
from analysis import pipeline_analysis
from llm import generate_response
from prompts import SYSTEM_PROMPT

DEALS_BOARD = os.getenv("DEALS_BOARD")
WORK_BOARD = os.getenv("WORK_ORDERS_BOARD")


def detect_intent(query: str):
    q = query.lower()

    # CROSS BOARD (highest priority)
    cross_keywords = [
        "convert",
        "converting",
        "conversion",
        "vs",
        "compare",
        "pipeline vs",
        "execution vs",
        "deal to work",
        "work order vs",
    ]

    if any(k in q for k in cross_keywords):
        return "cross_board"

    # WORK ORDER QUESTIONS
    work_keywords = [
        "work order",
        "execution",
        "delivery",
        "operations",
    ]

    if any(k in q for k in work_keywords):
        return "work_orders"

    # DEFAULT
    return "deals"


def run_agent(user_query):

    trace = []
    trace.append("🧠 Understanding query")

    intent = detect_intent(user_query)
    trace.append(f"Intent detected: {intent}")

    deals_df = None
    work_df = None

    # ---------- DEALS ----------
    if intent in ["deals", "cross_board"]:
        trace.append("📥 Fetching Deals board")
        deals = fetch_board(DEALS_BOARD, trace)
        deals_df = clean_dataframe(deals)

    # ---------- WORK ORDERS ----------
    if intent in ["work_orders", "cross_board"]:
        trace.append("📥 Fetching Work Orders board")
        work = fetch_board(WORK_BOARD, trace)
        work_df = clean_dataframe(work)

    # ---------- ANALYSIS ----------
    trace.append("📊 Running business intelligence analysis")

    result = {}

    if deals_df is not None:
        result["pipeline"] = pipeline_analysis(deals_df)

    if work_df is not None:
        result["work_orders"] = {
            "total_work_orders": len(work_df)
        }

    if deals_df is not None and work_df is not None:

        deals_count = len(deals_df)
        work_count = len(work_df)

        conversion_rate = (
            round((work_count / deals_count) * 100, 2)
            if deals_count > 0 else 0
        )

        result["conversion_analysis"] = {
            "deals": deals_count,
            "work_orders": work_count,
            "conversion_rate_percent": conversion_rate
        }

    # ---------- LLM ----------
    prompt = f"""
{SYSTEM_PROMPT}

IMPORTANT:
Use ONLY the provided data.
Do NOT invent numbers.

User Question:
{user_query}

DATA:
{result}

Provide founder-level business insight covering:
- revenue
- pipeline health
- sector performance when possible.
"""

    answer = generate_response(prompt)

    return answer, trace
