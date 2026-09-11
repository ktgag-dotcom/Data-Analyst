# U.S. City Transportation Access and Cost Analysis

A one-day data analytics exercise comparing U.S. cities on car-free transportation access and housing affordability, with an optional cab-fare benchmark for cities where historical taxi trip data is available.

## Business questions
- Which cities are most practical for car-free living?
- Which cities combine transit/walking access with lower housing-cost burden?
- How sensitive are city rankings to the weighting assumptions?
- If a traveler enters a city, trip distance, and cab fare, is the quoted cost below, within, or above the usual range for comparable historical trips?

## Data
Prepare `data/city_metrics.csv` from U.S. Census ACS place-level data. Required columns: `city`, `state`, `transit_pct`, `walk_pct`, `no_vehicle_pct`, `median_gross_rent`, `median_household_income`.

For the optional cab checker, add `data/taxi_trips.csv` with `city`, `trip_miles`, and `total_fare`. Use an official city/open-data taxi source where available. The checker deliberately returns insufficient data instead of inventing a benchmark when comparable records are unavailable.

Raw large datasets are not intended to be committed.

## Method
The analysis engineers a rent-to-income measure, min-max normalizes indicators, reverses the housing-cost scale so higher means better, and creates three weighted scenarios: balanced, transit-heavy, and budget-heavy. Comparing scenario ranks provides a simple sensitivity analysis.

The cab checker uses distance-band matching and percentile benchmarking. A quote is compared with historical trips within roughly 20% of the requested distance (minimum half-mile window). The 25th to 75th percentile of fare-per-mile is treated as the usual range, with at least 30 comparable trips required.

All weights, score bands, distance tolerances, and minimum sample sizes are project assumptions rather than official standards.

## Run
```bash
pip install -r requirements.txt
python main.py
```

Outputs are written to `output/`, including ranked city data and charts.

## Portfolio skills
Python, pandas, feature engineering, normalization, composite indices, percentile ranking, sensitivity analysis, benchmark distributions, data-quality safeguards, SQL window functions, and visualization.

See `analysis_notes.txt` for an interview-study explanation of each method, why it is used, and how it is implemented here.