insert
	into
	dim_product_scd2 (
	    tiki_pid ,
		name,
		brand_name,
        origin,
		ingestion_dt_unix,
	    valid_from,
	    valid_to,
		is_current
)
select
	tiki_pid ,
    name,
		brand_name,
        origin,
	ingestion_dt_unix,
		  ingestion_dt_unix valid_from,
	    null valid_to,
	true  as is_current
from
	dim_product;