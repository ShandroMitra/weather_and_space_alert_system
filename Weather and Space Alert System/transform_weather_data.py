import pandas as pd
import random
from datetime import datetime
from weather_monitor import weatherapi,fetch_weather_batch


df = pd.DataFrame(fetch_weather_batch())


#rounding off all float cols
df = df.round({
    'temperature_celcius': 2,
    'humidity_%': 0,
    'dew_temperature_celcius': 2,
    'feels_like_temperature_celcius': 2,
    'wind_speed_kmph':2,
    'precipitation_%': 0,
    'precipitation_occured_mm': 2,
    'rain_mm': 2,
    'showers_mm': 2,
    'snowfall_mm': 2,
    'snow_depth_mm': 2,
    'mean_sea_level_pressure_hpa': 2,
    'surface_pressure_hpa': 1,
    'cloud_cover_%': 0,
    'visibility_m': 2,
    'evapotranspiration_mm': 3,
    'et0_fao_evapotranspiration_mm': 3,
    'vapour_pressure_deficit_kpa': 4
})


#add water strees index
df['water_stress_index'] = (
    df['evapotranspiration_mm'] / (df['precipitation_occured_mm'] + 0.01)  # Avoid div/0
).round(2)


# Add current datetime in the specified format
df['created_at'] = datetime.now()


#add column of check extreme condition or not
# List of dangerous/extreme weather codes
extreme_codes = []
if extreme_codes:
    df['extreme_weather_yn'] = df['weather_code'].isin(extreme_codes).map({True: 'Y', False: 'N'})
else:
    df['extreme_weather_yn'] = 'N/A'



#snowfall_yn column
df['snowfall_yn'] = 'N'
df.loc[df['snowfall_mm'] > 0, 'snowfall_yn'] = 'Y'


# rainfall_yn column
df['rainfall_yn'] = 'N'
df.loc[(df['rain_mm'] > 0) | (df['showers_mm'] > 0), 'rainfall_yn'] = 'Y'


# foggy_yn column
df['foggy_yn'] = 'N'
df.loc[df['visibility_m'] < 1000, 'foggy_yn'] = 'Y'


# effective_precipitation_mm based on sum of snowfall,rain and shower i mm
SNOW_TO_LIQUID_RATIO = 10
# Convert snowfall_mm to its water equivalent
df['snowfall_water_equivalent_mm'] = df['snowfall_mm'] / SNOW_TO_LIQUID_RATIO
df['effective_precipitation_mm'] = df['rain_mm'] + df['showers_mm'] + df['snowfall_water_equivalent_mm']


#creating unique_id
city_short_map = {
    'Delhi': 'DEL', 
    'Mumbai': 'MUM', 
    'Bengaluru': 'BLR', 
    'Hyderabad': 'HYD', 
    'Chennai': 'CHE',  
    'Kolkata': 'KOL',  
    'Ahmedabad': 'AMD',  
    'Pune': 'PUN',  
    'Jaipur': 'JAI', 
    'Lucknow': 'LKO'  
}
def generate_unique_id(row):
    city_short = city_short_map.get(row['city'], row['city'][:3].upper())
    weather_code_str = f"{int(row['weather_code']):02d}"  # pad weather code to 2 digits
    rand_num = f"{random.randint(0, 99):02d}"            # 2 digit random number
    dt = row['created_at']
    dt_str = dt.strftime('%d%m%y%H%M%S')                # DDMMYYHHMMSS 
    ms_str = f"{int(dt.microsecond / 10000):02d}"        # first 2 digits of milliseconds  
    unique_id = f"{city_short}-{weather_code_str}-{rand_num}-{dt_str}{ms_str}"
    return unique_id
df['unique_id'] = df.apply(generate_unique_id, axis=1)
#unique id = 3 leters city shortform-weather_code-random 2 digit-date time in format DDMMYYHHMMSSMS


# #convert to boolean field if needed
# for col in ['rainfall_yn', 'snowfall_yn', 'foggy_yn']:
#     df[col] = df[col].map({'Y': True, 'N': False})


#weather type column based on weather code (WMO standard)
# Step 1: Create the mapping dictionary
weather_code_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    4: "Fog",
    5: "Drizzle",
    6: "Rain",
    7: "Showers",
    8: "Snow",
    9: "Rain and snow",
    10: "Sleet",
    11: "Hail",
    12: "Thunderstorm",
    13: "Duststorm",
    14: "Sandstorm",
    15: "Smoke",
    16: "Volcanic ash",
    17: "Windstorm",
    18: "Tornado",
    19: "Freezing rain",
    20: "Mist",
    21: "Light rain",
    22: "Moderate rain",
    23: "Heavy rain",
    24: "Light snow",
    25: "Moderate snow",
    26: "Heavy snow",
    27: "Light sleet",
    28: "Moderate sleet",
    29: "Heavy sleet",
    30: "Light hail",
    31: "Moderate hail",
    32: "Heavy hail",
    33: "Light thunderstorm",
    34: "Moderate thunderstorm",
    35: "Heavy thunderstorm",
    36: "Light duststorm",
    37: "Moderate duststorm",
    38: "Heavy duststorm",
    39: "Light sandstorm",
    40: "Moderate sandstorm",
    41: "Heavy sandstorm",
    42: "Light smoke",
    43: "Moderate smoke",
    44: "Heavy smoke",
    45: "Light volcanic ash",
    46: "Moderate volcanic ash",
    47: "Heavy volcanic ash",
    48: "Light windstorm",
    49: "Strong windstorm",
    50: "Severe windstorm",
    51: "Light tornado",
    52: "Moderate tornado",
    53: "Heavy tornado",
    54: "Light freezing rain",
    55: "Moderate freezing rain",
    56: "Heavy freezing rain",
    57: "Light mist",
    58: "Moderate mist",
    59: "Heavy mist",
    60: "Light rain and snow",
    61: "Moderate rain and snow",
    62: "Heavy rain and snow",
    63: "Light sleet and snow",
    64: "Moderate sleet and snow",
    65: "Heavy sleet and snow",
    66: "Light hail and snow",
    67: "Moderate hail and snow",
    68: "Heavy hail and snow",
    69: "Light thunderstorm with rain",
    70: "Moderate thunderstorm with rain",
    71: "Heavy thunderstorm with rain",
    72: "Light thunderstorm with snow",
    73: "Moderate thunderstorm with snow",
    74: "Heavy thunderstorm with snow",
    75: "Light thunderstorm with sleet",
    76: "Moderate thunderstorm with sleet",
    77: "Heavy thunderstorm with sleet",
    78: "Light thunderstorm with hail",
    79: "Moderate thunderstorm with hail",
    80: "Heavy thunderstorm with hail",
    81: "Light thunderstorm with dust",
    82: "Moderate thunderstorm with dust",
    83: "Heavy thunderstorm with dust",
    84: "Light thunderstorm with sand",
    85: "Moderate thunderstorm with sand",
    86: "Heavy thunderstorm with sand",
    87: "Light thunderstorm with smoke",
    88: "Moderate thunderstorm with smoke",
    89: "Heavy thunderstorm with smoke",
    90: "Light thunderstorm with volcanic ash",
    91: "Moderate thunderstorm with volcanic ash",
    92: "Heavy thunderstorm with volcanic ash",
    93: "Light windstorm with rain",
    94: "Strong windstorm with rain",
    95: "Severe windstorm with rain",
    96: "Light windstorm with snow",
    97: "Strong windstorm with snow",
    98: "Severe windstorm with snow",
    99: "Light windstorm with sleet",
    100: "Severe windstorm with sleet"
}
df['weather_type'] = df['weather_code'].map(weather_code_map)


# drop if null available in important columns-
df = df.dropna(subset=['city','temperature_celcius', 'humidity_%', 'wind_speed_kmph','weather_code','precipitation_occured_mm','created_at','extreme_weather_yn'])


#ordering columns
sorted_columns = [
    # Location Info
    'city',   
    # Core Weather Measurements
    'temperature_celcius',
    'feels_like_temperature_celcius',
    'dew_temperature_celcius',
    'humidity_%',
    'vapour_pressure_deficit_kpa',
    'wind_speed_kmph',    
    # Precipitation & Snowfall
    'precipitation_%',
    'precipitation_occured_mm',
    'rain_mm',
    'showers_mm',
    'rainfall_yn',
    'snowfall_mm',
    'snow_depth_mm',
    'snowfall_yn',
    'effective_precipitation_mm',
    # Fog & Visibility
    'foggy_yn',
    'visibility_m',
    'cloud_cover_%',
    # Pressure & Wind
    'mean_sea_level_pressure_hpa',
    'surface_pressure_hpa',
    # Evaporation
    'evapotranspiration_mm',
    'et0_fao_evapotranspiration_mm',
    # Weather Code & Classification
    'weather_code',
    'weather_type',   
    # Environmental Indicators
    'water_stress_index',
    'extreme_weather_yn',
    # 🕒 Timestamps
    'unique_id',
    'created_at'
]
df = df[sorted_columns]

# for debugging
print(df)