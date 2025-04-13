from flask import Flask, request
import os
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
from telegram import Update

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# Stylish Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "╭━━━╮╱╱╱╱╱╱╱╱╭╮\n┃╭━╮┃╱╱╱╱╱╱╱╱┃┃\n┃╰━━┳━━┳━━┳━━┫┃╭┳━━┳━╮\n╰━━╮┃┃━┫╭╮┃╭╮┃╰╯┫┃━┫╭╯\n┃╰━╯┃┃━┫╰╯┃╰╯┃╭╮┫┃━┫┃\n╰━━━┻━━┻━╮┣━╮┻╯╰┻━━┻╯\n╱╱╱╱╱╱╱╭━╯┃\n╱╱╱╱╱╱╱╰━━╯\n\n🤖 I'm *JARVIS Dev Assistant Bot* created by *Navneet Dabwal*!\n\nSend /help to see what I can do.",
        parse_mode="Markdown"
    )

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available Commands:\n/start - Welcome Message\n/help - This Message")

# Default echo message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am alive and ready! Try /start or /help.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        application.update_queue.put_nowait(update)
        return "ok"
    return "Bot is alive!"

@app.before_first_request
def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/"
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
