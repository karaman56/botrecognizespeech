import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from dotenv import load_dotenv

from common_utils import get_dialogflow_response

logger = logging.getLogger(__name__)


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


def handle_message(update, context, dialogflow_project_id):
    """Обработчик всех текстовых сообщений"""
    user_message = update.message.text
    user_id = str(update.message.from_user.id)
    session_id = f"tg-{user_id}"

    logger.info(f"Message from Telegram user {user_id} (session: {session_id}): {user_message}")

    response = get_dialogflow_response(
        project_id=dialogflow_project_id,
        session_id=session_id,
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
    logger.exception("Telegram bot error:")


def main():
    """Запуск бота"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    load_dotenv()

    telegram_bot_token = os.environ["BOT_TOKEN"]
    dialogflow_project_id = os.environ["DIALOGFLOW_PROJECT_ID"]
    chat_id = os.environ["CHAT_ID"]

    updater = Updater(telegram_bot_token , use_context=True)
    dp = updater.dispatcher
    dp.add_error_handler(error_handler)

    def safe_handle_message(update, context):
        try:
            handle_message(update, context, dialogflow_project_id)
        except Exception:
            logger.exception("Ошибка обработки сообщения Telegram:")
            update.message.reply_text("Sorry, an error occurred while processing your request.")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, safe_handle_message))

    logger.info("Бот запущен...")

    Bot(token=telegram_bot_token ).send_message(
        chat_id=chat_id,
        text="✅ <b>Telegram Bot запущен</b>",
        parse_mode='HTML'
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        logger.error(f"Отсутствует обязательная переменная окружения: {e}")
        raise
    except Exception:
        logger.exception("Critical error in Telegram bot:")
        try:
            load_dotenv()
            telegram_bot_token  = os.getenv["BOT_TOKEN"]
            chat_id = os.getenv["CHAT_ID"]
            if telegram_bot_token  and chat_id:
                Bot(token=telegram_bot_token ).send_message(
                    chat_id=chat_id,
                    text="🔥 <b>Telegram Bot Critical Error</b>\n\nПроизошла критическая ошибка",
                    parse_mode='HTML'
                )
        except Exception:
            logger.exception("Не удалось отправить сообщение об ошибке:")
        raise