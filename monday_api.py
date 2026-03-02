import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MONDAY_API_KEY")
URL = "https://api.monday.com/v2"


def fetch_board(board_id, trace):

    if trace is not None:
        trace.append(f"🌐 API CALL → monday.com board {board_id}")

    board_id_str = str(board_id).strip()

    query = f"""
    {{
      boards(ids: {board_id_str}) {{
        items_page(limit: 500) {{
          items {{
            name
            column_values {{
              column {{ title }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        URL,
        json={"query": query},
        headers={
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        }
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Monday API error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Detect GraphQL errors
    if "errors" in data:
        raise RuntimeError(f"GraphQL Error: {data['errors']}")

    boards = data.get("data", {}).get("boards", [])

    if not boards:
        raise RuntimeError(
            f"No board returned. Check board id or permissions."
        )

    items = boards[0]["items_page"]["items"]

    records = []

    for item in items:
        row = {"Item Name": item["name"]}

        for col in item["column_values"]:
            title = col["column"]["title"]
            row[title] = col["text"]

        records.append(row)

    if trace is not None:
        trace.append(f"✅ Retrieved {len(records)} rows")

    return records
