
CREATE TABLE dim_product_scd2 (
    id SERIAL PRIMARY KEY,
    tiki_pid INT,
    name TEXT ,
    brand_name TEXT,
    origin text,
    ingestion_dt_unix BIGINT,
    valid_from BIGINT,
    valid_to BIGINT,
    is_current BOOLEAN DEFAULT true
);