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
    # TODO: add the name to the database or whatever
    await update.message.reply_text("now please enter your email")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add the email to the database
    await update.message.reply_text("now please enter your password")
    return PASS

async def get_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add the password to the database
    await update.message.reply_text("thank you, your form is completed")

    # TODO: show the submitted data
    # await update.message.reply_text(f"{}")

    return ConversationHandler.END
  
def main():
    print("bot is running")

    app = Application.builder().token(API_TOKEN).build()

    app.add_handlers([
        CommandHandler("start", start),
        # CommandHandler("register", register),
        ConversationHandler(
            entry_points=[CommandHandler("register", register)],
            states={
                NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
                EMAIL: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_email)],
                PASS: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_pass)]
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    ])

    print("bot is polling")
    app.run_polling()

if __name__ == "__main__":
    main()