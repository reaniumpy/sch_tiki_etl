import pandas as pd
import datetime
from datetime_unix import string_to_unix

def compare_dataframes(df_old, df_new, unique_column, date_columns=None):
    # Initial load
    if df_old.empty:
        unique_id_insert =  df_new.loc[:,unique_column]
        unique_id_update =  pd.DataFrame(None)
        df_compare = None

        return unique_id_insert, unique_id_update, df_compare 
    
    # if date_columns:
        # df_old[date_columns] = df_old[date_columns].applymap(string_to_unix)
        # df_new[date_columns] = df_new[date_columns].applymap(string_to_unix)

    # Create a tracking hash for old and new dataframes
    columns_to_join_old = df_old.columns

    df_old['tracking_hash'] = df_old[columns_to_join_old].astype(str).apply(''.join, axis=1)
    df_new['tracking_hash'] = df_new[columns_to_join_old].astype(str).apply(''.join, axis=1)


    # Merge old and new dataframes
    df_compare = df_new.merge(df_old, on=unique_column, how='left', indicator=True)

    # Track new entries
    df_compare['is_new'] = df_compare['_merge'].eq('left_only')

    # Track changes
    df_compare['is_change'] = (df_compare['tracking_hash_x'] != df_compare['tracking_hash_y']) & ~df_compare['tracking_hash_y'].isna()

    # Convert date strings to UNIX timestamps in the old dataframe if date_columns is provided

    unique_id_update =  df_compare.loc[df_compare['is_change'],unique_column]
    unique_id_insert =  df_compare.loc[df_compare['is_new'],unique_column]
    return unique_id_insert, unique_id_update, df_compare 


def string_to_unix(string_date):
    if pd.isnull(string_date):
        return 0
    try:
        # Try parsing with milliseconds
        date_obj = datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        try:
            # Try parsing without milliseconds
            date_obj = datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                # Try parsing with the format MM/DD/YYYY
                date_obj = datetime.datetime.strptime(string_date, '%m/%d/%Y')
            except ValueError:
                try:
                    # Try parsing with the format YYYY-MM-DD
                    date_obj = datetime.datetime.strptime(string_date, '%Y-%m-%d')
                except ValueError as e:
                    print(f"Error: {e}")
                    return None
    unix_time = int(date_obj.timestamp())
    return unix_time