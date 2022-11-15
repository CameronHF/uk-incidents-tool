SELECT
index AS 'recipe_index',
LOWER(REPLACE(REPLACE(REPLACE(REPLACE(title, " ", "-"),",", ""),"'", ""), "&", "and")) AS recipe
FROM fact_tables.recipe_in_menu as rm
LEFT JOIN dimensions.recipe_dimension AS rd
ON rd.sk_recipe = rm.fk_recipe
WHERE week = '2022-Wweek_number'
AND rd.country = 'MARKET'
AND (charge_reason IS NULL
OR charge_reason = 'premium')
GROUP BY 1, 2
ORDER BY 1 asc;