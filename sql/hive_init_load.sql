--https://github.com/cartershanklin/hive-scd-examples/blob/master/hive_type2_scd.sql
CREATE TABLE fact_sales_scd2 (
    id SERIAL PRIMARY KEY,
    tiki_pid INT,
    price INT,
    quantity_sold_value INT,
    ingestion_dt_unix BIGINT,
    valid_from BIGINT,
    valid_to BIGINT,
    current_flag BOOLEAN DEFAULT true
);

-- raw_sales into fact_sales_scd2

-- INIT LOAD

insert
	into
	fact_sales_scd2 (
	    tiki_pid ,
		price,
		quantity_sold_value ,
		ingestion_dt_unix,
	    valid_from,
	    valid_to,
		current_flag
)
select
	tiki_pid ,
	price,
	quantity_sold_value ,
	ingestion_dt_unix,
		  ingestion_dt_unix valid_from,
	    null valid_to,
	true  as current_flag
from
	raw_sales;