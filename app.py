import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "╭━━━━━━━[ 𝗝𝗔𝗥𝗩𝗜𝗦 ]━━━━━━━╮\n"
        "│   Your Personal AI Assistant\n"
        "│\n"
        "│   Developed by: 𝗡𝗔𝗩𝗡𝗘𝗘𝗧 𝗗𝗔𝗕𝗪𝗔𝗟\n"
        "│   Telegram: @JARVIS_AI_NK_BOT\n"
        "│   Status: ✅ Online\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        "Use /help to explore my powers!"
    )
    await update.message.reply_text(msg)

application.add_handler(CommandHandler("start", start))

@app.route("/")
def home():
    return "Bot is live and healthy!"

@app.before_first_request
def activate_bot():
    import threading
    def run_bot():
        application.run_polling()
    threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
