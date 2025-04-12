import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI setup
openai.api_key = OPENAI_API_KEY

# Flask app
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "Jarvis Bot is Running!"

# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = "Navneet Dabwal"
    fancy_name = "𝙉𝙖𝙫𝙣𝙚𝙚𝙩 𝘿𝙖𝙗𝙬𝙖𝙡"
    msg = f"Hello, I am Jarvis — your Dev Assistant Bot!\n\nDeveloped by: *{fancy_name}*"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide code to explain.")
        return

    code = " ".join(context.args)
    prompt = f"Explain this code:\n\n{code}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Something went wrong.")

# Telegram application
async def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("explain", explain))
    await app.run_polling()

def start_bot():
    asyncio.run(run_bot())

# Thread to run Telegram bot
threading.Thread(target=start_bot).start()

# Run Flask app (Render looks for port)
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
