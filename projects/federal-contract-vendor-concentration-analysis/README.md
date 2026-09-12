# Federal Contract Vendor Concentration Analysis

## Question
How concentrated is federal contract spending among major vendors, and which agencies depend most heavily on a small number of suppliers?

This project analyzes federal procurement awards using Python and SQL. It aggregates contract obligations by agency and recipient, calculates vendor spending shares, measures concentration with the Herfindahl-Hirschman Index (HHI), calculates Top-5 supplier concentration, and builds Pareto curves showing how quickly contract spending accumulates among the largest vendors.

## Data
Use federal contract award data from USAspending.gov. Download one fiscal year of contract awards and save the prepared extract as `data/contracts.csv`.

Required columns:
- `recipient_name`
- `awarding_agency`
- `obligated_amount`

Useful optional fields include `awarding_subagency`, `naics_code`, `naics_description`, `award_type`, `start_date`, `end_date`, and recipient state.

Raw government exports are intentionally not committed because they can be large. See `data/README.md` for preparation instructions.

## Questions answered
- Which agencies have the largest contract obligations?
- Which vendors receive the most contract dollars within each agency?
- What share of agency spending goes to the five largest vendors?
- How concentrated is each agency's supplier base according to HHI?
- How many ranked vendors are needed to account for most spending?
- Which agencies warrant closer supplier-dependency review?

## Methods
The analysis uses grouped aggregation, vendor-share calculations, Pareto/cumulative-share analysis, Top-N concentration ratios, HHI, project-defined concentration classifications, SQL aggregation, and SQL window functions.

The HHI and concentration categories are analytical tools. High concentration does not by itself demonstrate poor procurement practice because specialized programs can legitimately depend on a limited supplier market.

## Run
```bash
pip install -r requirements.txt
python main.py
```

Outputs are written to `output/`, including vendor-level summaries, agency concentration metrics, a SQLite database, and charts.

## Portfolio angle
This exercise demonstrates procurement and spend analytics, supplier concentration measurement, risk-oriented interpretation, Python data transformation, SQL, window functions, cumulative distributions, and stakeholder-friendly visualization using real public-sector contract data.
