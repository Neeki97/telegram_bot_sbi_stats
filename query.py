
date = ''

query_partners = f"""
        SELECT ox_payments.name as payment_name,
        COUNT(ox_sell_transactions.ox_payment_id) AS quantity,
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM ox_sell_transactions 
        JOIN ox_payments
        ON ox_sell_transactions.ox_payment_id=ox_payments.id
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE 
        AND status = 'finished' 
        AND ox_sell_transactions."type"='sell'
        GROUP BY ox_payments."name" """


query_regions = f"""
        SELECT ox_locations."administrativeArea" AS regions,
        COUNT(ox_locations."id") as quantity_sale,
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM ox_sell_transactions
        INNER JOIN ox_sell_records
        ON ox_sell_transactions.ox_sell_id = ox_sell_records.ox_sell_id
        INNER JOIN ox_locations
        ON ox_sell_records.ox_location_id = ox_locations.id
        WHERE ox_sell_transactions."type"='sell'
        AND DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE
        AND status='finished'
        AND ox_locations."type"='shop'
        GROUP BY ox_locations."administrativeArea" """


query_stores = f"""
        SELECT subquery.*
        FROM (
        SELECT ox_locations."name" as store,
        COUNT(ox_locations."id") as quantity_sale, 
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM "ox_sell_transactions"
        INNER JOIN ox_sell_records
        ON ox_sell_transactions.ox_sell_id = ox_sell_records.ox_sell_id
        INNER JOIN ox_locations
        ON ox_sell_records.ox_location_id = ox_locations."id"
        WHERE ox_sell_transactions."type"='sell' 
        AND DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE
        AND ox_sell_transactions."status" = 'finished'
        AND ox_locations."type" = 'shop'
        GROUP BY ox_locations."name"
        ORDER BY quantity_sale DESC
        LIMIT 10) AS subquery """


query_sallers = f"""
        SELECT subquery.*
        FROM (
        SELECT (ox_users."firstName" || ' ' || ox_users."lastName") as full_name,
        COUNT(ox_users."id") as quantity_sale,  
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_sum,
        ox_locations."name" as store 
        FROM ox_users
        INNER JOIN ox_sells
        ON ox_users."id" = ox_sells.ox_user_id
        INNER JOIN ox_sell_records
        ON ox_sells."id" = ox_sell_records.ox_sell_id
        INNER JOIN ox_sell_transactions
        ON ox_sells."id" = ox_sell_transactions.ox_sell_id
        INNER JOIN ox_locations
        ON ox_sell_records.ox_location_id = ox_locations."id"
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE 
        AND ox_sell_transactions."type" ='sell'
        AND ox_sell_transactions.status = 'finished'
        AND ox_locations."type" = 'shop'
        GROUP BY ox_users."firstName", ox_users."lastName", ox_locations."name"
        ORDER BY quantity_sale DESC
        LIMIT 10) AS subquery """


query_devices = f"""
        SELECT subquery.*
        FROM (
        SELECT ox_variants."name" as device,
        COUNT(ox_variants."id") as количество_продаж, 
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as общая_сумма
        FROM ox_variants
        INNER JOIN ox_sell_records
        ON ox_variants."id" = ox_sell_records.ox_variant_id
        INNER JOIN ox_sell_transactions
        ON ox_sell_transactions.ox_sell_id = ox_sell_records.ox_sell_id
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE
        AND ox_sell_transactions."type"='sell'
        AND ox_sell_transactions.status='finished'
        GROUP BY device
        ORDER BY количество_продаж DESC
        LIMIT 10) AS subquery """