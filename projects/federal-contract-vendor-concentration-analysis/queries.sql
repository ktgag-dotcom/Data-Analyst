-- Total positive contract obligations by agency
SELECT awarding_agency,
       SUM(obligated_amount) AS total_spend
FROM federal_contracts
WHERE obligated_amount > 0
GROUP BY awarding_agency
ORDER BY total_spend DESC;

-- Largest vendors across the analyzed dataset
SELECT recipient_name,
       SUM(obligated_amount) AS total_spend
FROM federal_contracts
WHERE obligated_amount > 0
GROUP BY recipient_name
ORDER BY total_spend DESC
LIMIT 20;

-- Rank vendors separately within each agency
WITH vendor_spend AS (
    SELECT awarding_agency,
           recipient_name,
           SUM(obligated_amount) AS vendor_spend
    FROM federal_contracts
    WHERE obligated_amount > 0
    GROUP BY awarding_agency, recipient_name
), ranked AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY awarding_agency
               ORDER BY vendor_spend DESC
           ) AS vendor_rank
    FROM vendor_spend
)
SELECT awarding_agency, recipient_name, vendor_spend, vendor_rank
FROM ranked
WHERE vendor_rank <= 5
ORDER BY awarding_agency, vendor_rank;

-- Vendor spending share within each agency using window functions
WITH vendor_spend AS (
    SELECT awarding_agency,
           recipient_name,
           SUM(obligated_amount) AS vendor_spend
    FROM federal_contracts
    WHERE obligated_amount > 0
    GROUP BY awarding_agency, recipient_name
)
SELECT awarding_agency,
       recipient_name,
       vendor_spend,
       vendor_spend / SUM(vendor_spend) OVER (PARTITION BY awarding_agency) AS vendor_share
FROM vendor_spend
ORDER BY awarding_agency, vendor_spend DESC;
