-- Insert new records into dim_product_scd2
INSERT INTO dim_product_scd2 (tiki_pid, name, brand_name, origin, ingestion_dt_unix, valid_from, valid_to, is_current)
SELECT
    dim_product.tiki_pid,
    dim_product.name,
    dim_product.brand_name,
    dim_product.origin,
    dim_product.ingestion_dt_unix,
    dim_product.ingestion_dt_unix,
    NULL,
    true
FROM
    dim_product
LEFT JOIN
    dim_product_scd2 ON dim_product.tiki_pid = dim_product_scd2.tiki_pid
WHERE
    dim_product_scd2.id IS NULL; -- Only insert if the record doesn't exist in dim_product_scd2

-- Update existing records in dim_product_scd2
UPDATE
    dim_product_scd2
SET
    valid_to = sub.ingestion_dt_unix,
    is_current = false
FROM (
    SELECT
        dim_product.tiki_pid,
        dim_product_scd2.id,
        dim_product.*
    FROM
        dim_product
    JOIN
        dim_product_scd2 ON dim_product.tiki_pid = dim_product_scd2.tiki_pid
    WHERE
        (dim_product.name <> dim_product_scd2.name OR dim_product.origin <> dim_product_scd2.origin OR dim_product.brand_name <> dim_product_scd2.brand_name)
        AND dim_product_scd2.valid_to IS null
        and is_current = true
) AS sub
WHERE
    dim_product_scd2.id = sub.id;

   
   
INSERT INTO dim_product_scd2 (tiki_pid, name, brand_name, origin, ingestion_dt_unix, valid_from, valid_to, is_current)
SELECT
    distinct dim_product.tiki_pid,
    dim_product.name,
    dim_product.brand_name,
    dim_product.origin,
    dim_product.ingestion_dt_unix,
    dim_product.ingestion_dt_unix,
    NULL, -- Set valid_to to NULL for new records
    true
FROM
    dim_product
LEFT JOIN
    dim_product_scd2 ON dim_product.tiki_pid = dim_product_scd2.tiki_pid
WHERE
    (dim_product.name <> dim_product_scd2.name OR dim_product.origin <> dim_product_scd2.origin OR dim_product.brand_name <> dim_product_scd2.brand_name)
    --AND dim_product_scd2.id IS null
    and dim_product_scd2.is_current = true
