import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_stylish = "『 𝗡𝗮𝘃𝗻𝗲𝗲𝘁 𝗗𝗮𝗯𝘄𝗮𝗹 』"
    msg = (
        f"✨ Welcome to *JARVIS AI Assistant Bot* ✨\n\n"
        f"Developer: *{name_stylish}*\n"
        f"Bot: `@JARVIS_AI_NK_BOT`\n"
        f"Powered by: *Python × Flask × Telegram API*\n\n"
        f"_Type /help to see what I can do._"
    )
    await update.message.reply_markdown(msg)

# /help handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available Commands:\n/start - Introduction\n/help - List of commands")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put_nowait(update)
        return "OK"
    return "Bot is running!"

async def set_webhook():
    webhook_url = os.environ.get("RENDER_EXTERNAL_URL")
    if webhook_url:
        await application.bot.set_webhook(f"{webhook_url}/")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=10000)
