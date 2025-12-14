import os
import random
import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8423784042:AAGpypFyrHrT-SxAIzgf2R_8pFiLV2UjceE")  # Use your bot's token here
GROUP_CHAT_ID = os.getenv("-1002530598502")  # Use your group's chat ID here
bot = Bot(token=BOT_TOKEN)

stickers = [
    "CAACAgQAAxkBAAKmh2f5EBjXCvSqjGVYDT9P7yjKW6_IAAKOCAACi9XoU5p5sAokI77kNgQ",
    "CAACAgQAAxkBAAKmimf5EB9GTlXRtwVB3ez1nBUKzf69AAKaDAACfx_4UvcUEDj6i_r9NgQ",
    "CAACAgQAAxkBAAKmjWf5ECecZUCJtSeuqsaaVWILpTuyAALICwACG86YUDSKklgR_M5FNgQ",
    "CAACAgIAAxkBAAKmkGf5EDBgwnSDovUPpQGsTjMQdU69AAL4DAACNyx5S6FYW3VBcuj4NgQ"
]

def get_random_prediction():
    return random.choice(["Big", "Small"])

def send_prediction():
    # Assuming `period` is obtained correctly, you can bypass the error by handling it manually
    period = random.randint(1000, 9999)  # Replace with actual logic for fetching period

    prediction = get_random_prediction()
    message = f"[WINGO 1MINUTE]\nPeriod {period}\nChoose - {prediction}"
    bot.send_message(chat_id=GROUP_CHAT_ID, text=message)

    # Send sticker with a 50% chance, using the sticker ID directly
    if random.random() < 0.5:
        bot.send_sticker(chat_id=GROUP_CHAT_ID, sticker=random.choice(stickers))

    print(f"Sent: {message}")

# APScheduler to run the job periodically
def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_prediction, 'interval', minutes=1)
    scheduler.start()

# Telegram Bot /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Running ✅")

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))

# Run scheduler in background
start_scheduler()

# Run bot polling
updater.start_polling()
