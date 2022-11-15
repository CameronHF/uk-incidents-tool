SELECT lower(cul.name) AS ingredient_name, cul.code AS culinary_sku, recipe_card_name
FROM Impala.dimensions.culinary_sku_dimension AS cul
LEFT JOIN materialized_views.remps_sku_sku AS sku ON cul.code = sku.code
WHERE cul.status = 'Active'
AND cul.brand IN ('COUNTRY')
AND cul.market = 'GB'
AND lower(cul.name) LIKE '%REPLACE_ME%'
GROUP BY 1,2,3