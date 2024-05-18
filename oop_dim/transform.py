import os
import httpx
import pandas as pd
from datetime import datetime
import sys

module_path = os.path.abspath(os.path.join('..')) + '/my_utils'
if module_path not in sys.path:
    sys.path.append(module_path)

import util_minio

class Transform:
    def __init__(self, minio_handler, bucket_name):
        self.minio_handler = minio_handler
        self.bucket_name = bucket_name

    def execute(self, csv_name, columns):
        df = self.minio_handler.download_to_dataframe(self.bucket_name, f'raw/{csv_name}')
        df_transformed = df[columns]
        return df_transformed

# Example usage:
if __name__ == "__main__":
    csv_name = 'raw_116532_1716029308.csv'
    minio_handler = MinioHandler()
    bucket_name = "tiki"
    transform_columns = ["tiki_pid", "name", "brand_name", "origin", 'ingestion_date', 'ingestion_dt_unix']

    transformer = Transform(minio_handler, bucket_name)
    df_transformed = transformer.execute(csv_name, transform_columns)
    dict_storage_options = {'endpoint_url': 'http://localhost:9000', 'key': 'minioadmin', 'secret': '12345678'}
    df_transformed.to_parquet('s3://tiki/curated/dim_product/', storage_options=dict_storage_options, partition_cols=['ingestion_date'])
