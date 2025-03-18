def get_weather_emoji(description):
    description = description.lower()
    if "ясно" in description:
        return "☀️"
    elif "облачно" in description or "дым" in description:
        return "☁️"
    elif "легкий туман" in description:
        return "🌤"
    elif "значительная облачность" in description:
        return "🌥"
    elif "небольшой снегопад" in  description or "cнежно-ледяная изморось" in description or "легкий снег" in description:
        return "🌨"
    else:
        return "🌥"