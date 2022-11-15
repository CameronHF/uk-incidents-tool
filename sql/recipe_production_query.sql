WITH all_cte AS (
SELECT dd.hellofresh_week AS weeknumber
         , sc.box_id          AS box_id
         , CASE WHEN sc.box_id LIKE 'GB%' THEN LEFT (sc.box_id, 10)
                WHEN sc.box_id LIKE 'GN%' THEN LEFT (sc.box_id, 9)
            END
            AS clean_box_id
         , RIGHT (sc.box_id, 2) AS MB
         , CONCAT(sc.line, ' - All') AS line
         , dd.day_name AS 'production-day'
         , CONCAT(sc.city, ' - All') AS site
         , LEFT (sc.`event_timestamp`, 10) AS 'date'
         , RIGHT (LEFT (sc.`event_timestamp`, 19), 8) AS 'time'
FROM
   materialized_views.p2l_inducted_boxes AS sc
    LEFT JOIN dimensions.date_dimension AS dd
ON dd.sk_date = sc.fk_imported_at
WHERE
    sc.country = 'UK'
AND LEFT(sc.`event_timestamp`, 10) BETWEEN 'REPLACE_START' AND 'REPLACE_END' -- replace these
ORDER BY
    sc.`event_timestamp` DESC

    )

SELECT weeknumber,
       (ac.box_id),
       clean_box_id,
       CASE WHEN mb NOT IN ('B1', 'B2') THEN ''
           ELSE mb
           END AS mb_indicator,
       oc.customer_id                           AS customer_id,
       line,
       oc.production_day,
       oc.delivery_day,
       courier,
       site,
       brand,
       dc,
       ac.`date`,
       ac.`time`,
       box_value,
       box_size,
       number_of_recipes,
       REPLACE_ADDON_OR_RECIPE

FROM all_cte AS ac
         INNER JOIN uploads.gb_order_creation_live AS oc
                    ON oc.box_id = ac.box_id
         LEFT JOIN bob_live_gb_anon.customer AS ca ON oc.customer_id = ca.id_customer
         LEFT JOIN bob_live_gb_anon.customer_address AS aa ON aa.fk_customer = oc.customer_id

REPLACE_WHERE