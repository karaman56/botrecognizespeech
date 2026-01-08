import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from dotenv import load_dotenv

from common_utils import get_dialogflow_response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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


def error_handler(update, context, chat_id):
    """Обработчик ошибок бота"""
    error_msg = f"Telegram bot error: {context.error}"
    logger.error(error_msg)

    context.bot.send_message(
        chat_id=chat_id,
        text=f"🚨 <b>Telegram Bot Error</b>\n\n{error_msg}",
        parse_mode='HTML'
    )


def main():
    """Запуск бота"""
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    dialogflow_project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    chat_id = os.getenv("CHAT_ID")

    try:
        updater = Updater(bot_token, use_context=True)
        dp = updater.dispatcher

        dp.add_error_handler(lambda update, context: error_handler(update, context, chat_id))

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))

        dp.add_handler(MessageHandler(Filters.text,
                                      lambda update, context: handle_message(update, context, dialogflow_project_id)))

        logger.info("Бот запущен...")

        updater.bot.send_message(
            chat_id=chat_id,
            text="✅ <b>Telegram Bot запущен</b>",
            parse_mode='HTML'
        )

        updater.start_polling()
        updater.idle()

    except Exception as e:
        error_msg = f"Critical error starting bot: {e}"
        logger.error(error_msg)

        bot = Bot(token=bot_token)
        bot.send_message(
            chat_id=chat_id,
            text=f"🔥 <b>Telegram Bot Critical Error</b>\n\n{error_msg}",
            parse_mode='HTML'
        )
        raise


if __name__ == "__main__":
    main()