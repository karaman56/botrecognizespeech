import vk_api
import os
import logging
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from google.cloud import dialogflow_v2beta1 as dialogflow
from dotenv import load_dotenv

load_dotenv()


VK_TOKEN = os.getenv("VK_TOKEN")
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BOT_TOKEN_TG = os.getenv("BOT_TOKEN_TG")
CHAT_ID = os.getenv("CHAT_ID")


def send_to_telegram(message):
    """Отправляет сообщение в Telegram бот"""
    if not BOT_TOKEN_TG or not CHAT_ID:
        return

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN_TG}/sendMessage"
        data = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.post(url, data=data, timeout=5)
    except:
        pass


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

        logger.info(f"DialogFlow ответил:")
        logger.info(f"  Запрос: {message}")
        logger.info(f"  Ответ: {response.query_result.fulfillment_text}")
        logger.info(f"  Is Fallback: {response.query_result.intent.is_fallback}")

        return response

    except Exception as e:
        error_msg = f"DialogFlow error: {e}"
        logger.error(error_msg)

        send_to_telegram(f"⚠️ <b>VK Bot - DialogFlow Error</b>\n\n{error_msg}")

        return None


def send_message(vk, user_id, message):
    """Отправляет сообщение пользователю VK"""
    try:
        vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=get_random_id()
        )
        logger.info(f"Отправлено сообщение пользователю {user_id}")
    except Exception as e:
        error_msg = f"Ошибка отправки сообщения VK: {e}"
        logger.error(error_msg)

        send_to_telegram(f"⚠️ <b>VK Bot - Send Error</b>\n\n{error_msg}")


def main():
    """Запуск VK бота с DialogFlow"""
    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        logger.info("VK бот с DialogFlow запущен...")

        send_to_telegram("✅ <b>VK Bot запущен</b>")

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                user_message = event.text

                logger.info(f"Новое сообщение от {user_id}: {user_message}")

                if user_message.lower() in ['/start', 'start', 'начать']:
                    send_message(vk, user_id,
                                 "🤖 Привет! Я умный бот с искусственным интеллектом!\n"
                                 "Задай мне любой вопрос, и я постараюсь помочь.\n"
                                 "Если я не отвечу - значит передам твой вопрос оператору!"
                                 )
                    continue

                if user_message.lower() in ['/help', 'help', 'помощь']:
                    send_message(vk, user_id,
                                 "💡 Я могу ответить на различные вопросы:\n"
                                 "• Как устроиться на работу\n"
                                 "• Проблемы с паролем\n"
                                 "• Удаление аккаунта\n"
                                 "• И многое другое!\n\n"
                                 "⚠️ Если я не отвечу на ваш вопрос - его увидят операторы техподдержки!"
                                 )
                    continue

                response = get_dialogflow_response(
                    project_id=DIALOGFLOW_PROJECT_ID,
                    session_id=str(user_id),
                    message=user_message,
                    language_code='ru'
                )

                if response and response.query_result.fulfillment_text:
                    if not response.query_result.intent.is_fallback:
                        bot_response = response.query_result.fulfillment_text
                        send_message(vk, user_id, bot_response)
                        logger.info(f"✅ Отправлен ответ (не fallback)")
                    else:
                        logger.info(f"🤫 Пропускаем ответ (fallback intent)")
                else:
                    logger.info(f"🤫 Пропускаем ответ (ошибка DialogFlow)")

    except Exception as e:

        error_msg = f"Critical error starting VK bot: {e}"
        send_to_telegram(f"🔥 <b>VK Bot Critical Error</b>\n\n{error_msg}")
        raise


if __name__ == "__main__":
    main()