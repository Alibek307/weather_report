import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pandas_profiling import ProfileReport

df = pd.read_csv("weather_data.csv")

def clean_temperature(temp_str):
    if isinstance(temp_str, str):
        return float(temp_str.replace('°', ''))
    return temp_str

df['Current Temp'] = df['Current Temp'].apply(clean_temperature)
df['High Temp'] = df['High Temp'].apply(clean_temperature)
df['Low Temp'] = df['Low Temp'].apply(clean_temperature)

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

print(df.head())

print(df.describe())

daily_avg_temp = df["Current Temp"].resample("D").mean()
print(daily_avg_temp)

plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Current Temp'], label='Текущая температура')
plt.plot(df.index, df['High Temp'], label='Максимальная температура')
plt.plot(df.index, df['Low Temp'], label='Минимальная температу')
plt.title('Изменение температуры')
plt.xlabel('Дата')
plt.ylabel('Температура (°С)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Humidity'], label='Влажность', color='green')
plt.title('Изменение влажности')
plt.xlabel('Дата')
plt.ylabel('Влажность (%)')
plt.legend()
plt.grid(True)
plt.show

numeric_df = df.select_dtypes(include=['float64', 'int64'])

plt.figure(figsize=(8, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title('Корреляция между параметрами')
plt.show()

profile = ProfileReport(df, title='Анализ погодных данных')
profile.to_file("weather_report.html")
