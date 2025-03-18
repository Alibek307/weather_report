from weather_fetch import fetch_weathercast
import pandas as pd
import os
import datetime
import asyncio

weather = fetch_weathercast()

def save_weather_data(weather):
    data = {
        "Date": [pd.Timestamp.now()],
        "Current Temp": [weather["current_temp"]],
        "Description": [weather["description"]],
        "High Temp": [weather["high_temp"]],
        "Low Temp": [weather["low_temp"]],
        "Humidity": [weather["humidity"]],
        "Feels Like": [weather["feels_like"]],
        "Location": [weather["location"]],
        "aqi": [weather["aqi"]]
    }
    df = pd.DataFrame(data)

    if os.path.exists("weather_data.csv"):
        df.to_csv("weather_data.csv", mode='a', index=False, header=False)
    else:
        df.to_csv("weather_data.csv", mode='w', index=False, header=True)

async def save_data_task(context):
    try:
        now = datetime.datetime.now()
        if now.minute == 0:
            weather = fetch_weathercast()
            save_weather_data(weather)
            print(f"Data saved! {now}")
    except Exception as e:
            print(f"Ошибка: {e}")

async def scheduler():
    while True:
        now = datetime.datetime.now()
        next_hour = (now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1))
        wait_time = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_time)
        await save_data_task(None)

async def main():
    await scheduler()

if __name__ == "__main__":
    asyncio.run(main())