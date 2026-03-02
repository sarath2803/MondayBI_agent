# import pandas as pd
# import re

# def normalize_currency(val):
#     if val is None:
#         return 0

#     val = str(val).lower().replace(",", "")

#     if "k" in val:
#         return float(re.sub("[^0-9.]", "", val)) * 1000

#     return float(re.sub("[^0-9.]", "", val) or 0)


# def clean_dataframe(records):

#     df = pd.DataFrame(records)

#     for col in df.columns:
#         df[col] = df[col].fillna("")

#     # normalize sector
#     if "Sector" in df.columns:
#         df["Sector"] = df["Sector"].str.title()

#     # normalize amount/value
#     for col in ["Amount", "Value"]:
#         if col in df.columns:
#             df[col] = df[col].apply(normalize_currency)

#     return df


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

    # Auto-detect money columns
    # for col in df.columns:
    #     if any(k in col.lower() for k in ["value", "amount", "deal"]):
    #         df[col] = df[col].apply(normalize_currency)
    for col in df.columns:
        if any(k in col.lower() for k in ["value", "amount", "deal"]):
            df[col] = df[col].apply(normalize_currency)

    return df