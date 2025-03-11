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
        message_id=update.effective_message.id
    )
  
async def echo(update: Update, context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text=update.effective_message.text,
        message_id = update.effective_message.id,
    )


def main():
    print("bot is running")

    # important
    app = Application.builder().token(API_TOKEN).build()

    # command handlers
    start_handler = CommandHandler("start","s","START", start)
    
    # message handlers
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # adding the command handelrs to the bot
    app.add_handler(start_handler)

    # adding the message handelrs to the bot
    app.add_handler(echo_handler)

    print("bot is polling")
    app.run_polling()
    

if __name__ == "__main__":
    main()


