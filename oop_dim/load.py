import pandas as pd
from sqlalchemy import create_engine

class Load:
    def __init__(self, db_url, storage_options):
        self.engine = create_engine(db_url)
        self.storage_options = storage_options

    def execute(self, parquet_path, table_name):
        df = pd.read_parquet(parquet_path, storage_options=self.storage_options)
        latest_row = df.loc[df['ingestion_dt_unix'].idxmax()]
        df_latest = df[df['ingestion_dt_unix'] == latest_row['ingestion_dt_unix']]
        df_latest.to_sql(table_name, self.engine, if_exists='replace', index=False)
        print(df_latest)

# Example usage:
if __name__ == "__main__":
    db_url = 'postgresql://my_user:my_password@localhost:35432/dw_tiki'
    parquet_path = 's3://tiki/curated/dim_product/ingestion_date=2024-05-18'
    table_name = 'dim_product'
    storage_options = {'endpoint_url': 'http://localhost:9000', 'key': 'minioadmin', 'secret': '12345678'}

    loader = Load(db_url, storage_options)
    loader.execute(parquet_path, table_name)