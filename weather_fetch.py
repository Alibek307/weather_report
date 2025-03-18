from bs4 import BeautifulSoup
import requests

def fetch_weathercast(): #парсит данные о погоде с сайта weather.com
    url = "https://weather.com/ru-RU/weather/today/l/5ead5bf0831e9c4adb7cc4a4f0f66264147a55a24823c075c67035cbfb30724b"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    current_temp_element = soup.select_one('span[data-testid="TemperatureValue"]')
    current_temp = current_temp_element.text if current_temp_element else "Ошибка, не удалось найти текущую температуру"

    description_element = soup.select_one('div[data-testid="wxPhrase"]')
    description = description_element.text if description_element else "Ошибка, не удалось найти состояние"

    humidity_element = soup.select_one('span[data-testid="PercentageValue"]')
    humidity = humidity_element.text if humidity_element else "Ошибка, не удалось найти влажность"

    feels_like_element = soup.select_one('div[data-testid="FeelsLikeSection"] span[data-testid="TemperatureValue"]')
    feels_like = feels_like_element.text if feels_like_element else "Ошибка, не удалось найти влажность"

    location_element = soup.select_one('h1[class="CurrentConditions--location--yub4l"]')
    location = location_element.text if location_element else "Ошибка, не удалось найти локацию"

    air_quality_index_element = soup.select_one('text[data-testid="DonutChartValue"]')
    aqi = air_quality_index_element.text if air_quality_index_element else "Ошибка, не удалось найти индекс"

    hi_lo_temp = soup.select_one('div.CurrentConditions--tempHiLoValue--Og9IG')
    if hi_lo_temp:
        spans = hi_lo_temp.find_all('span', {'data-testid': 'TemperatureValue'})
        high_temp = spans[0].text if len(spans) > 0 else "Ошибка, не удалось найти макс температуру"
        low_temp = spans[1].text if len(spans) > 1 else "Ошибка, не удалось найти мин температуру"
    else:
        high_temp, low_temp = "Ошибка, не удалось найти макс температуру", "Ошибка, не удалось найти мин температуру"

    return{
        "current_temp": current_temp,
        "description": description,
        "high_temp": high_temp,
        "low_temp": low_temp,
        "humidity": humidity,
        "feels_like": feels_like,
        "location": location,
        "aqi": aqi
    }

# добавить смайлики
# добавить команду на погоду на неделю
# добавить локализацию(англ, каз)
# добавить выбор локации