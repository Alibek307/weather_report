from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update, ReplyKeyboardMarkup
from weather_fetch import fetch_weathercast
from get_weather_emoji import get_weather_emoji

TELEGRAM_TOKEN = "YOUR_TOKEN"
TELEGRAM_CHAT_ID = "497292801"

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #команда /weather, отправляет текущую спаршенную погоду 
    weather = fetch_weathercast()
    emoji = get_weather_emoji(weather["description"])
    message = (
        f"{emoji} Прогноз на сегодня: {weather['location']}\n"
        f"Температура воздуха: {weather['current_temp']}\n"
        f"{weather['description']} {weather['high_temp']}/ {weather['low_temp']}\n"
        f"Влажность: {weather['humidity']}\n"
        f"Ощущается как: {weather['feels_like']}\n"
        f"Индекс качества воздуха: {weather['aqi']}"
    )
    await update.message.reply_text(message)
    print("Message sent!")

async def send_schedule(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    update = job.data
    await weather_command(update, context)    

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(
        send_schedule,
        interval=3600,
        first=0,
        chat_id=chat_id,
        data=update
    )
    await update.message.reply_text("Ежечасная рассылка погоды запущена.")
    print("Schedule enabled!")

async def stopschedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text("Ежечасная рассылка погоды остановлена.")
    print("Schedule disabled!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = ReplyKeyboardMarkup(
        [["/weather", "/schedule"], ["/stopschedule"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        "Выберите команду:",
        reply_markup=menu
    )

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("stopschedule", stopschedule_command))

    application.run_polling()

if __name__ == "__main__":
    main()
