from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests
import os

# Load API keys from environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Store user subscriptions
subscribed_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /subscribe to get weather updates.")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in subscribed_users:
        subscribed_users.add(user_id)
        await update.message.reply_text("You have subscribed to weather updates!")
    else:
        await update.message.reply_text("You are already subscribed.")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        await update.message.reply_text("You have unsubscribed from weather updates!")
    else:
        await update.message.reply_text("You are not subscribed.")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = " ".join(context.args) if context.args else "London"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        await update.message.reply_text(f"Error: {response.get('message', 'Unknown error')}")
        return

    weather_info = f"Weather in {location}:\n" \
                   f"Temperature: {response['main']['temp']}°C\n" \
                   f"Condition: {response['weather'][0]['description']}"
    await update.message.reply_text(weather_info)

async def broadcast(context: ContextTypes.DEFAULT_TYPE):
    for user_id in subscribed_users:
        try:
            await context.bot.send_message(chat_id=user_id, text="Daily Weather Update!")
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

# Main function to run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("weather", weather))

    # Daily job for weather updates
    app.job_queue.run_repeating(broadcast, interval=86400)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("7502094362:AAHe3TN7avvxuSdf23iImBV-o1f_NsNsPYM")
WEATHER_API_KEY = os.getenv("https://api.meteomatics.com/2024-11-21T00:00:00Z/t_2m:C/52.520551,13.461804/html")
