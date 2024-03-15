merge into fact_sales_scd2
using (
  -- The base staging data.
  select
    raw_sales.tiki_pid as join_key,
    raw_sales.* from raw_sales

  union all

  -- Generate an extra row for changed records.
  -- The null join_key means it will be inserted.
  select
    null, raw_sales.*
  from
    raw_sales join fact_sales_scd2 on raw_sales.tiki_pid = fact_sales_scd2.tiki_pid
  where
    ( raw_sales.quantity_sold_value <> fact_sales_scd2.quantity_sold_value )
    and fact_sales_scd2.valid_to  is null
) sub
on sub.join_key = fact_sales_scd2.tiki_pid
when matched
  and sub.quantity_sold_value <> fact_sales_scd2.quantity_sold_value
  then update set valid_to = 444444444 -- change to ingestion time
when not matched
  then insert values (100,sub.tiki_pid, sub.price, sub.quantity_sold_value,sub.ingestion_dt_unix, 444444444,null,true);