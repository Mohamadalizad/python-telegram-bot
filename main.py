from decouple import config
from telegram import Update
from telegram.ext import Application , CommandHandler, ContextTypes , MessageHandler, filters

API_TOKEN = config("API_TOKEN")

# made command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # daryaft chat_id and message_id
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Register form",
    )
  
def main():
    print("bot is running")

    # important
    app = Application.builder().token(API_TOKEN).build()

    # command handlers
    start_handler = CommandHandler("start", start)

    # adding the command handelrs to the bot
    app.add_handler(start_handler)

    print("bot is polling")
    app.run_polling()

if __name__ == "__main__":
    main()