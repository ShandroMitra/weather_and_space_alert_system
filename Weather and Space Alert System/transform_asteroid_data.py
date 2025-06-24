import pandas as pd
from datetime import datetime
from nasa_asteroid_tracker import neosapi
#convert to dataframe
df = pd.DataFrame(neosapi())

# Data Type Optimization
df['asteroid_name'] = df['asteroid_name'].astype(str)
df['nasa_id'] = df['nasa_id'].astype(str)
df['nasa_site_url'] = df['nasa_site_url'].astype(str)
df['closest_approach_distance_km'] = df['closest_approach_distance_km'].round(2)
df['velocity_kmph'] = df['velocity_kmph'].round(2)
df['diameter_min_m'] = df['diameter_min_m'].round(2)
df['diameter_max_m'] = df['diameter_max_m'].round(2)
df['is_potentially_hazardous'] = df['is_potentially_hazardous'].astype(bool)

#time ordering -> YYYY-MM-DD HH:MM:SS
df['closest_approach_time_to_earth_IST'] = pd.to_datetime(df['closest_approach_time_to_earth_IST'], format='%Y-%b-%d %H:%M')

#chnage UTC to IST
df['closest_approach_time_to_earth_IST'] = df['closest_approach_time_to_earth_IST'] + pd.Timedelta(hours=5, minutes=30)

#cleaning asteroid_name column and removing brackets
df['asteroid_name'] = df['asteroid_name'].astype(str).str.replace(r'[()]', '', regex=True)

#uppercasing asteroid_name
df['asteroid_name'] = df['asteroid_name'].str.upper()  

#drop duplicates
df.drop_duplicates(subset=['nasa_id','asteroid_name'], inplace=True)

#unique column as data_id combination of date time(including miliseconds)
def generate_data_id(nasa_id):
    now = datetime.now()
          # Format date and time as required (2 digits each, millisecond 2 digits)
    dt_str = now.strftime('%d%m%y%H%M%S')  # day, month, year, hour, minute, second (all 2 digits)
    ms_str = str(int(now.microsecond / 10000)).zfill(2)  # convert microsecond to 2 digit millisecond (0-99)
    return f"{nasa_id}-{dt_str}{ms_str}"

df['data_id'] = df['nasa_id'].apply(generate_data_id)

#add data_load_datetime for data load date and time 
df['created_at'] = datetime.now()

#verify url
df['nasa_site_url'] = df['nasa_site_url'].apply(
    lambda url: url if isinstance(url, str) and url.startswith('https://') and 'nasa.gov' in url
    else 'url not found'
)

#handle is_potentially_hazardous boolean value and fill if needed
def determine_hazard(row):
    val = str(row['is_potentially_hazardous']).strip().lower()
    if val in ['true', 'yes', '1']:
        return True
    elif val in ['false', 'no', '0']:
        return False
    else:
        # Check other conditions
        if (row['diameter_max_m'] > 150 and
            row['closest_approach_distance_km'] < 1000000 and
            row['velocity_kmph'] > 8000):
            return True
        else:
            return False
df['is_potentially_hazardous'] = df.apply(determine_hazard, axis=1)


#handle duplicate values with data_id
if not df['data_id'].is_unique:
    print("Duplicates found in 'data_id'. Removing duplicate rows, keeping the first occurrence.")
    df = df.drop_duplicates(subset=['data_id'], keep='first')
else:
    print("All 'data_id' values are unique.")

# for debugging
print(df)