import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Thêm API Key của OpenAI và Telegram Bot
OPENAI_API_KEY = "your_openai_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Cấu hình OpenAI API
openai.api_key = OPENAI_API_KEY

# Hàm xử lý tin nhắn
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        # Gửi yêu cầu tới OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
        # Gửi phản hồi lại người dùng
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("Có lỗi xảy ra khi kết nối API!")

# Hàm bắt đầu bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Xin chào! Tôi là bot hỗ trợ bởi ChatGPT. Hãy hỏi tôi bất kỳ điều gì!")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Xử lý các lệnh
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Bắt đầu bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
