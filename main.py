import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("BOT_TOKEN або OPENAI_API_KEY не встановлено!")

openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logging.info(f"Повідомлення від @{update.effective_user.username}: {user_message}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти корисний Telegram-бот. Відповідай чітко і українською."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error("Помилка OpenAI:", exc_info=True)
        reply = f"На жаль, сталася помилка: {e}"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Бот запущено.")
    app.run_polling()

if __name__ == "__main__":
    main()
