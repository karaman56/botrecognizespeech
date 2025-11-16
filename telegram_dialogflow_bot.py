import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow_v2beta1 as dialogflow

# Настройки
BOT_TOKEN = "5435821594:AAGa7Cg-Vw4JAL4-ztTcJMfQpoA-8yLoyZg"
DIALOGFLOW_PROJECT_ID = "mybott-turm"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/monster/.config/gcloud/application_default_credentials.json"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dialogflow_response(project_id, session_id, message, language_code='ru'):
    """Получаем ответ от DialogFlow - ТОЧНО как в рабочем тесте"""
    try:
        # Создаем клиент - как в рабочем тесте
        session_client = dialogflow.SessionsClient()

        # Создаем сессию - как в рабочем тесте
        session = session_client.session_path(project_id, session_id)

        # Создаем запрос - как в рабочем тесте
        text_input = dialogflow.TextInput(text=message, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        # Отправляем запрос - как в рабочем тесте
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        logger.info(f"DialogFlow успешно ответил:")
        logger.info(f"  Запрос: {message}")
        logger.info(f"  Ответ: {response.query_result.fulfillment_text}")
        logger.info(f"  Интент: {response.query_result.intent.display_name}")
        logger.info(f"  Уверенность: {response.query_result.intent_detection_confidence}")

        return response

    except Exception as e:
        logger.error(f"DialogFlow error: {e}")
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

    # Получаем ответ от DialogFlow - ТОЧНО как в рабочем тесте
    response = get_dialogflow_response(
        project_id=DIALOGFLOW_PROJECT_ID,
        session_id=user_id,  # Используем ID пользователя как session_id
        message=user_message,
        language_code='en'  # Используем английский как в рабочем тесте
    )

    if response and response.query_result.fulfillment_text:
        bot_response = response.query_result.fulfillment_text
    else:
        bot_response = "Sorry, I couldn't process your request. Please try again."

    # Отправляем ответ пользователю
    update.message.reply_text(bot_response)


def main():
    """Запуск бота"""
    # Создаем Updater
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрируем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Запускаем бота
    logger.info("Бот запущен...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()