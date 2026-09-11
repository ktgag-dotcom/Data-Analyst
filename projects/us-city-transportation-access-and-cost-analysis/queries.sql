-- Highest-scoring cities
SELECT city, state, ROUND(balanced_score, 2) AS score, balanced_rank
FROM city_livability
ORDER BY balanced_score DESC
LIMIT 20;

-- Cities with strong transit use and relatively low housing-cost burden
SELECT city, state, transit_pct, ROUND(rent_income_ratio * 100, 1) AS rent_income_pct
FROM city_livability
WHERE transit_pct > 10
ORDER BY rent_income_ratio ASC;

-- Average profile by project-defined classification
SELECT classification,
       COUNT(*) AS cities,
       ROUND(AVG(transit_pct), 2) AS avg_transit_pct,
       ROUND(AVG(no_vehicle_pct), 2) AS avg_no_vehicle_pct,
       ROUND(AVG(rent_income_ratio) * 100, 1) AS avg_rent_income_pct
FROM city_livability
GROUP BY classification
ORDER BY AVG(balanced_score) DESC;

-- Compare each city's transportation score with other cities in the same state
SELECT city, state, balanced_score,
       RANK() OVER (PARTITION BY state ORDER BY balanced_score DESC) AS state_rank
FROM city_livability
ORDER BY state, state_rank;

-- Cities whose rank changes most when affordability is emphasized
SELECT city, state, balanced_rank, budget_heavy_rank,
       ABS(balanced_rank - budget_heavy_rank) AS rank_change
FROM city_livability
ORDER BY rank_change DESC
LIMIT 20;
