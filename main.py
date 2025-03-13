from decouple import config
from telegram import Update
from telegram.ext import Application , CommandHandler, ContextTypes , MessageHandler, filters

API_TOKEN = config("API_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Register form",
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Test"
    )
    # username
    # email
    # pass
  
def main():
    print("bot is running")

    app = Application.builder().token(API_TOKEN).build()

    app.add_handlers([
        CommandHandler("start", start),
        CommandHandler("register", register)
    ])

    print("bot is polling")
    app.run_polling()

if __name__ == "__main__":
    main()