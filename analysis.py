import pandas as pd

def pipeline_analysis(deals_df, sector=None):

    df = deals_df.copy()

    # ---------- detect columns ----------
    sector_column = None
    value_column = None

    for col in df.columns:
        if "sector" in col.lower():
            sector_column = col

        if any(k in col.lower() for k in ["value", "amount", "revenue"]):
            value_column = col

    # ---------- numeric safety ----------
    if value_column:
        df[value_column] = pd.to_numeric(
            df[value_column], errors="coerce"
        ).fillna(0)

    # ---------- filter ----------
    if sector and sector_column:
        df = df[df[sector_column].str.contains(sector, case=False, na=False)]

    # ---------- metrics ----------
    deal_count = len(df)
    pipeline_value = df[value_column].sum() if value_column else 0

    # ---------- sector performance ----------
    sector_summary = {}

    if sector_column:
        sector_summary = (
            df.groupby(sector_column)
            .size()
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        )

    # ---------- health ----------
    if deal_count == 0:
        health = "No active pipeline."
    elif deal_count < 5:
        health = "Pipeline is small and may pose growth risk."
    else:
        health = "Pipeline volume appears healthy."

    return {
        "deal_count": int(deal_count),
        "pipeline_value": float(pipeline_value),
        "pipeline_health": health,
        "sector_performance": sector_summary,
    }
