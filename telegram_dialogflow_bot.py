import os
import logging
import requests  # ДОБАВИЛ: для отправки ошибок в Telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow_v2beta1 as dialogflow
from dotenv import load_dotenv

load_dotenv()

# ДОБАВИЛ: токен для бота-логгера
BOT_TOKEN = os.getenv("BOT_TOKEN")
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BOT_TOKEN_TG = os.getenv("BOT_TOKEN_TG")  # Токен бота для логов
CHAT_ID = os.getenv("CHAT_ID")  # ID куда отправлять логи


# ДОБАВИЛ: простая функция отправки ошибок в Telegram
def send_to_telegram(message):
    """Отправляет сообщение в Telegram бот"""
    if not BOT_TOKEN_TG or not CHAT_ID:
        return  # Если нет токена или chat_id - не отправляем

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN_TG}/sendMessage"
        data = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.post(url, data=data, timeout=5)
    except:
        pass  # Игнорируем ошибки отправки


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dialogflow_response(project_id, session_id, message, language_code='ru'):
    """Получаем ответ от DialogFlow"""
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        text_input = dialogflow.TextInput(text=message, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        logger.info(f"DialogFlow успешно ответил:")
        logger.info(f"  Запрос: {message}")
        logger.info(f"  Ответ: {response.query_result.fulfillment_text}")

        return response

    except Exception as e:
        error_msg = f"DialogFlow error: {e}"
        logger.error(error_msg)

        # ДОБАВИЛ: отправляем ошибку DialogFlow в Telegram
        send_to_telegram(f"⚠️ <b>Telegram Bot - DialogFlow Error</b>\n\n{error_msg}")

        return None


def start(update, context):
    """Обработчик команды /start"""
    update.message.reply_text(
        "🤖 Hello! I'm an AI bot with DialogFlow.\n"
        "Just write me something in English and I'll answer!"
    )


def help_command(update, context):
    """Обработчик команды /help"""
    update.message.reply_text(
        "💡 Just write any message in English and I'll answer using AI!\n"
        "Commands:\n"
        "/start - start conversation\n"
        "/help - show this help"
    )


def handle_message(update, context):
    """Обработчик всех текстовых сообщений"""
    user_message = update.message.text
    user_id = str(update.message.from_user.id)

    logger.info(f"Message from user {user_id}: {user_message}")

    response = get_dialogflow_response(
        project_id=DIALOGFLOW_PROJECT_ID,
        session_id=user_id,
        message=user_message,
        language_code='en'
    )

    if response and response.query_result.fulfillment_text:
        bot_response = response.query_result.fulfillment_text
    else:
        bot_response = "Sorry, I couldn't process your request. Please try again."

    update.message.reply_text(bot_response)


def error_handler(update, context):
    """Обработчик ошибок бота"""
    error_msg = f"Telegram bot error: {context.error}"
    logger.error(error_msg)

    send_to_telegram(f"🚨 <b>Telegram Bot Error</b>\n\n{error_msg}")


def main():
    """Запуск бота"""
    try:
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        # ДОБАВИЛ: добавляем обработчик ошибок
        dp.add_error_handler(error_handler)

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

        logger.info("Бот запущен...")


        send_to_telegram("✅ <b>Telegram Bot запущен</b>")

        updater.start_polling()
        updater.idle()

    except Exception as e:
        error_msg = f"Critical error starting bot: {e}"
        send_to_telegram(f"🔥 <b>Telegram Bot Critical Error</b>\n\n{error_msg}")
        raise


if __name__ == "__main__":
    main()