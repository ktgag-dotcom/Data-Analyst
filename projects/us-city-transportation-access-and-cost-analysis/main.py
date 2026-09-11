from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)


def normalize(series):
    series = pd.to_numeric(series, errors="coerce")
    spread = series.max() - series.min()
    if spread == 0:
        return pd.Series(0.5, index=series.index)
    return (series - series.min()) / spread


def analyze_cities(filename=DATA / "city_metrics.csv"):
    df = pd.read_csv(filename)
    required = ["city", "state", "transit_pct", "walk_pct", "no_vehicle_pct",
                "median_gross_rent", "median_household_income"]
    df = df.dropna(subset=required).copy()
    df = df[(df["median_gross_rent"] > 0) & (df["median_household_income"] > 0)]

    df["rent_income_ratio"] = (df["median_gross_rent"] * 12) / df["median_household_income"]
    df["transit_score"] = normalize(df["transit_pct"])
    df["walk_score"] = normalize(df["walk_pct"])
    df["no_vehicle_score"] = normalize(df["no_vehicle_pct"])
    df["affordability_score"] = 1 - normalize(df["rent_income_ratio"])

    scenarios = {
        "balanced": (.30, .25, .20, .25),
        "transit_heavy": (.45, .25, .20, .10),
        "budget_heavy": (.20, .20, .15, .45),
    }
    for name, weights in scenarios.items():
        t, nv, w, a = weights
        df[f"{name}_score"] = 100 * (t*df.transit_score + nv*df.no_vehicle_score + w*df.walk_score + a*df.affordability_score)
        df[f"{name}_rank"] = df[f"{name}_score"].rank(ascending=False, method="min").astype(int)

    df["percentile"] = df["balanced_score"].rank(pct=True) * 100
    df["classification"] = pd.cut(df["balanced_score"], [-1, 40, 60, 75, 101],
        labels=["Car-Dependent", "Difficult", "Good", "Excellent"])
    return df.sort_values("balanced_score", ascending=False)


def check_cab_fare(city, miles, fare, filename=DATA / "taxi_trips.csv"):
    if not Path(filename).exists():
        return {"status": "insufficient data", "message": "No taxi benchmark data is available."}
    if miles <= 0 or fare < 0:
        raise ValueError("Miles must be greater than zero and fare cannot be negative.")

    trips = pd.read_csv(filename)
    trips = trips[(trips["city"].str.casefold() == city.casefold()) & (trips["trip_miles"] > 0) & (trips["total_fare"] >= 0)].copy()
    tolerance = max(0.5, miles * 0.20)
    peers = trips[trips["trip_miles"].between(max(0.01, miles-tolerance), miles+tolerance)].copy()
    if len(peers) < 30:
        return {"status": "insufficient data", "message": "Fewer than 30 comparable historical trips."}

    peers["fare_per_mile"] = peers["total_fare"] / peers["trip_miles"]
    q25, median, q75 = peers["fare_per_mile"].quantile([.25, .50, .75])
    rate = fare / miles
    result = "Below usual range" if rate < q25 else "Above usual range" if rate > q75 else "Within usual range"
    return {"status": "ok", "comparison": result, "your_rate": rate, "typical_median_rate": median,
            "typical_fare_low": q25*miles, "typical_fare_high": q75*miles, "peer_trips": len(peers)}


def create_charts(df):
    top = df.head(15).sort_values("balanced_score")
    plt.figure(figsize=(9, 7))
    plt.barh(top["city"] + ", " + top["state"], top["balanced_score"])
    plt.xlabel("Transportation access and affordability score")
    plt.title("Top Cities for Car-Free Livability")
    plt.tight_layout()
    plt.savefig(OUTPUT / "city_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.scatter(df["balanced_score"], df["rent_income_ratio"]*100, alpha=.65)
    plt.xlabel("Transportation access score")
    plt.ylabel("Annual median rent / median household income (%)")
    plt.title("Transportation Access vs Housing Cost Burden")
    plt.tight_layout()
    plt.savefig(OUTPUT / "access_vs_cost.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    cities = analyze_cities()
    cities.to_csv(OUTPUT / "city_rankings.csv", index=False)
    create_charts(cities)
    print(cities[["city", "state", "balanced_score", "balanced_rank", "classification"]].head(20).to_string(index=False))

    if (DATA / "taxi_trips.csv").exists():
        city = input("Cab-check city: ").strip()
        miles = float(input("Trip miles: "))
        fare = float(input("Total cab fare ($): "))
        print(check_cab_fare(city, miles, fare))
