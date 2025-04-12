
import os
import openai
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PORT = int(os.environ.get("PORT", 10000))

openai.api_key = OPENAI_API_KEY

application = Application.builder().token(TELEGRAM_TOKEN).build()

@app.route("/")
def home():
    return "Jarvis Bot is Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey Developer!\n\n"
        "I am Jarvis — your personal AI Coding Assistant.\n"
        "Send me any code to explain, or use /optimize or /fix.\n\n"
        "Developed by\n𓆩 Navneet Dabwal 𓆪"
    )

async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful code explainer."},
            {"role": "user", "content": f"Explain this code:\n{code}"}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

async def optimize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code optimizer."},
            {"role": "user", "content": f"Optimize this code:\n{code}"}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

async def fix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that fixes bugs in code."},
            {"role": "user", "content": f"Fix the bugs in this code:\n{code}"}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

def start_bot():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("optimize", optimize))
    application.add_handler(CommandHandler("fix", fix))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, explain))
    application.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=PORT)
    
