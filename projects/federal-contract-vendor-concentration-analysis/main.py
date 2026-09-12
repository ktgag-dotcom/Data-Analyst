from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "output"
CHARTS = OUTPUT / "charts"
OUTPUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)


def load_contracts(path=DATA / "contracts.csv"):
    df = pd.read_csv(path)
    required = ["recipient_name", "awarding_agency", "obligated_amount"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["obligated_amount"] = pd.to_numeric(df["obligated_amount"], errors="coerce")
    df = df.dropna(subset=required).copy()
    return df[df["obligated_amount"] > 0]


def concentration_analysis(df):
    vendor = (df.groupby(["awarding_agency", "recipient_name"], as_index=False)
                ["obligated_amount"].sum())
    vendor = vendor.rename(columns={"obligated_amount": "vendor_spend"})
    totals = vendor.groupby("awarding_agency")["vendor_spend"].transform("sum")
    vendor["vendor_share"] = vendor["vendor_spend"] / totals
    vendor = vendor.sort_values(["awarding_agency", "vendor_spend"], ascending=[True, False])
    vendor["vendor_rank"] = vendor.groupby("awarding_agency")["vendor_spend"].rank(method="min", ascending=False).astype(int)
    vendor["cumulative_share"] = vendor.groupby("awarding_agency")["vendor_share"].cumsum()
    vendor["share_squared"] = vendor["vendor_share"] ** 2

    hhi = vendor.groupby("awarding_agency", as_index=False)["share_squared"].sum().rename(columns={"share_squared": "hhi"})
    top5 = (vendor[vendor["vendor_rank"] <= 5].groupby("awarding_agency", as_index=False)
            ["vendor_share"].sum().rename(columns={"vendor_share": "top5_share"}))
    summary = hhi.merge(top5, on="awarding_agency")
    summary["total_spend"] = summary["awarding_agency"].map(vendor.groupby("awarding_agency")["vendor_spend"].sum())
    summary["vendor_count"] = summary["awarding_agency"].map(vendor.groupby("awarding_agency")["recipient_name"].nunique())

    def classify(value):
        if value >= .50: return "Very High"
        if value >= .25: return "High"
        if value >= .15: return "Moderate"
        return "Low"

    summary["concentration_level"] = summary["hhi"].apply(classify)
    return vendor, summary.sort_values("hhi", ascending=False)


def create_charts(vendor, summary):
    spend = summary.nlargest(12, "total_spend").sort_values("total_spend")
    plt.figure(figsize=(9, 7))
    plt.barh(spend["awarding_agency"], spend["total_spend"] / 1e9)
    plt.xlabel("Contract obligations ($ billions)")
    plt.title("Federal Contract Spending by Agency")
    plt.tight_layout()
    plt.savefig(CHARTS / "agency_spending.png", dpi=160)
    plt.close()

    concentrated = summary.nlargest(15, "hhi").sort_values("hhi")
    plt.figure(figsize=(9, 7))
    plt.barh(concentrated["awarding_agency"], concentrated["hhi"])
    plt.xlabel("HHI")
    plt.title("Vendor Concentration by Agency")
    plt.tight_layout()
    plt.savefig(CHARTS / "concentration_by_agency.png", dpi=160)
    plt.close()

    largest_agency = summary.nlargest(1, "total_spend")["awarding_agency"].iloc[0]
    curve = vendor[vendor["awarding_agency"] == largest_agency].reset_index(drop=True)
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(curve) + 1), curve["cumulative_share"] * 100)
    plt.axhline(80, linestyle="--")
    plt.xlabel("Vendors ranked by contract spending")
    plt.ylabel("Cumulative spending share (%)")
    plt.title(f"Pareto Curve: {largest_agency}")
    plt.tight_layout()
    plt.savefig(CHARTS / "pareto_curve.png", dpi=160)
    plt.close()


def save_sqlite(df):
    with sqlite3.connect(OUTPUT / "contracts.db") as conn:
        df.to_sql("federal_contracts", conn, if_exists="replace", index=False)


if __name__ == "__main__":
    contracts = load_contracts()
    vendors, agencies = concentration_analysis(contracts)
    vendors.to_csv(OUTPUT / "vendor_summary.csv", index=False)
    agencies.to_csv(OUTPUT / "concentration_metrics.csv", index=False)
    save_sqlite(contracts)
    create_charts(vendors, agencies)
    print(agencies[["awarding_agency", "hhi", "top5_share", "vendor_count", "concentration_level"]].head(20).to_string(index=False))
