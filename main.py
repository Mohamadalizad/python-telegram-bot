from decouple import config
from telegram import Update
from telegram.ext import Application , CommandHandler, ContextTypes , ConversationHandler, filters, MessageHandler

API_TOKEN = config("API_TOKEN")

NAME, EMAIL, PASS = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Register form",
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="welcome to the registration proccess, please tell me your name:",
    )
    return NAME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("registration canceled")
    return ConversationHandler.END

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{update.message.text}")
  
def main():
    print("bot is running")

    app = Application.builder().token(API_TOKEN).build()

    app.add_handlers([
        CommandHandler("start", start),
        # CommandHandler("register", register),
        ConversationHandler(entry_points=[CommandHandler("register", register)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            },
        fallbacks=[CommandHandler("cancel", cancel)],
        )
    ])

    print("bot is polling")
    app.run_polling()

if __name__ == "__main__":
    main()