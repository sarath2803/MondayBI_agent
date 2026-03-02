import pandas as pd
import re


def normalize_currency(val):
    if not val:
        return 0

    val = str(val).lower().replace(",", "").strip()

    # remove any non-digit/non-dot characters
    num = re.sub("[^0-9.]", "", val)

    # handle thousands shorthand
    if "k" in val:
        try:
            return float(num or 0) * 1000
        except ValueError:
            return 0

    # try converting to float, fall back to 0 on failure
    try:
        # some Python builds (weird locales) raise ValueError on "."
        return float(num or 0)
    except ValueError:
        return 0


def clean_dataframe(records):

    df = pd.DataFrame(records)

    # Fill missing values
    df = df.fillna("")

    # Normalize all text columns
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # Auto-detect sector column
    for col in df.columns:
        if "sector" in col.lower():
            df[col] = df[col].str.title()

    for col in df.columns:
        if any(k in col.lower() for k in ["value", "amount", "deal"]):
            df[col] = df[col].apply(normalize_currency)

    return df
