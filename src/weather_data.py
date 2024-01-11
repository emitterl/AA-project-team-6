import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 34.052235,
	"longitude": -118.243683,
	"start_date": "2018-04-25",
	"end_date": "2021-09-14",
	"hourly": ["temperature_2m", "weather_code"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {"time": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature"] = hourly_temperature_2m
hourly_data["weather_code"] = hourly_weather_code

hourly_dataframe = pd.DataFrame(data = hourly_data)

hourly_dataframe['time'] = hourly_dataframe['time'].dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')
print(hourly_dataframe['time'])

def convert_weather_code(code):
    mapping = {
        0.0: "Cloud development not observed or not observable",
        1.0: "Clouds generally dissolving or becoming less developed",
        2.0: "State of sky on the whole unchanged",
        3.0: "Clouds generally forming or developing",
        51.0: "Drizzle, not freezing, continuous",
        53.0: "Drizzle, not freezing, intermittent moderate",
        61.0: "Rain, not freezing, continuous",
        63.0: "Rain, not freezing, intermittent moderate",
        55.0: "Drizzle, not freezing, continuous",
        65.0: "Rain, not freezing, continuous"
    }
    return mapping.get(code, "Unknown")

hourly_dataframe['weather_description'] = hourly_dataframe['weather_code'].apply(convert_weather_code)
hourly_dataframe.drop('weather_code', axis=1, inplace=True)

print(hourly_dataframe)
