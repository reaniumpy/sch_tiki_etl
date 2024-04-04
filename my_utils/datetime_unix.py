import datetime
import pytz
import numpy as np
import pandas as pd

# Function to convert string to Unix timestamp
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