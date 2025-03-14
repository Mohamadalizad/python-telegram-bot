import bcrypt
import sqlite3
from decouple import config
from telegram import Update
from telegram.ext import Application , CommandHandler, ContextTypes , ConversationHandler, filters, MessageHandler
from email_validator import validate_email, EmailNotValidError

API_TOKEN = config("API_TOKEN")
DATABASE_NAME = "database.db"
NAME, EMAIL, PASS = range(3)

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    email TEXT,
    password TEXT
)
""")
conn.commit()
conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a registration form")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("welcome to the registration proccess, please tell me your name:")
    return NAME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("registration canceled")
    return ConversationHandler.END

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.text

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)", (user_id, name))
    conn.commit()
    conn.close()

    await update.message.reply_text("now please enter your email")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    email = update.message.text.strip()

    # validate the email
    try:
        valid = validate_email(email, check_deliverability=True)
        email = valid.email
    except EmailNotValidError:
        await update.message.reply_text("Your email is not valid!\n Please enter your email again")
        return EMAIL

    # TODO: send verification codes to that email

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE telegram_id = ?", (email, user_id))
    conn.commit()
    conn.close()

    await update.message.reply_text("now please enter your password")
    return PASS

async def get_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    password = update.message.text
    hashed = hash_password(password)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE telegram_id = ?", (hashed, user_id))
    conn.commit()

    await update.message.reply_text("thank you, your form is completed")

    # design choice: we could also make a dictionary and keep the data instead of fetching from the database now
    
    cursor.execute("SELECT name, email FROM users WHERE telegram_id = ?", (user_id, ))
    user = cursor.fetchone()
    conn.close()

    await update.message.reply_text(f"Submitted info:\nName: {user[0]}\nEmail: {user[1]}")

    return ConversationHandler.END
  
def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

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