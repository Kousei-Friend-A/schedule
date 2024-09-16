import requests
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler
from database import init_db, update_database, check_for_releases, create_schedule_message
from config import API_TOKEN, CHANNEL_ID, SUBSPLS_API_URL

def fetch_schedule():
    response = requests.get(SUBSPLS_API_URL)
    return response.json()

def update_schedule(update, context):
    schedule = fetch_schedule()
    update_database(schedule)  # Update the database with the fetched schedule
    check_for_releases(schedule)  # Check and update release statuses
    message = create_schedule_message()  # Create the message to send
    context.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.MARKDOWN)
    context.bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=update.message.message_id)

def main():
    init_db()  # Initialize the database
    updater = Updater(token=API_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('update_schedule', update_schedule))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
