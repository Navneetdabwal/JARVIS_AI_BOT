
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hey Developer!\n\n"
        "I am Jarvis — your personal AI Coding Assistant.\n"
        "Send me any code to explain, or use /optimize or /fix.\n\n"
        "Developed by\n𓆩 Navneet Dabwal 𓆪"
    )

async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful code explainer."},
            {"role": "user", "content": f"Explain this code:\n{code}"}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

async def optimize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code optimizer."},
            {"role": "user", "content": f"Optimize this code:\n{code}"}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

async def fix(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that fixes bugs in code."},
            {"role": "user", "content": f"Fix the bugs in this code:\n{code}"}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("optimize", optimize))
    app.add_handler(CommandHandler("fix", fix))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, explain))
    app.run_polling()

if __name__ == "__main__":
    main()
    
