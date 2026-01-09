import vk_api
import os
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from telegram import Bot
from dotenv import load_dotenv

from common_utils import get_dialogflow_response

logger = logging.getLogger(__name__)


def send_telegram_from_vk(message, bot_token_tg, chat_id):
    """Простая отправка в Telegram из VK бота"""
    bot = Bot(token=bot_token_tg)
    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='HTML'
    )


def send_message(vk, user_id, message, bot_token_tg, chat_id):
    """Отправляет сообщение пользователю VK"""
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=get_random_id()
    )
    logger.info(f"Отправлено сообщение пользователю {user_id}")


def handle_vk_message(vk, user_id, user_message, dialogflow_project_id, bot_token_tg, chat_id):
    """Обработка одного сообщения от пользователя VK"""
    session_id = f"vk-{user_id}"

    logger.info(f"Новое сообщение от VK user {user_id} (session: {session_id}): {user_message}")

    if user_message.lower() in ['/start', 'start', 'начать']:
        send_message(vk, user_id,
                     "🤖 Привет! Я умный бот с искусственным интеллектом!\n"
                     "Задай мне любой вопрос, и я постараюсь помочь.\n"
                     "Если я не отвечу - значит передам твой вопрос оператору!",
                     bot_token_tg, chat_id)
        return

    if user_message.lower() in ['/help', 'help', 'помощь']:
        send_message(vk, user_id,
                     "💡 Я могу ответить на различные вопросы:\n"
                     "• Как устроиться на работу\n"
                     "• Проблемы с паролем\n"
                     "• Удаление аккаунта\n"
                     "• И многое другое!\n\n"
                     "⚠️ Если я не отвечу на ваш вопрос - его увидят операторы техподдержки!",
                     bot_token_tg, chat_id)
        return

    try:
        response = get_dialogflow_response(
            project_id=dialogflow_project_id,
            session_id=session_id,
            message=user_message,
            language_code='ru'
        )

        if not response.query_result.fulfillment_text:
            logger.info(f"🤫 Пропускаем ответ (пустой ответ DialogFlow)")
            return

        if hasattr(response.query_result.intent, 'is_fallback'):
            if response.query_result.intent.is_fallback:
                logger.info(f"🤫 Пропускаем ответ (fallback intent)")
                return

        bot_response = response.query_result.fulfillment_text
        send_message(vk, user_id, bot_response, bot_token_tg, chat_id)
        logger.info(f"✅ Отправлен ответ")

    except Exception:
        logger.exception("DialogFlow error in VK bot:")
        send_telegram_from_vk("⚠️ <b>VK Bot - DialogFlow Error</b>\n\nОшибка при обращении к DialogFlow",
                              bot_token_tg, chat_id)


def main():
    """Запуск VK бота с DialogFlow"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    load_dotenv()

    vk_token = os.environ["VK_TOKEN"]
    dialogflow_project_id = os.environ["DIALOGFLOW_PROJECT_ID"]
    bot_token_tg = os.environ["BOT_TOKEN_TG"]
    chat_id = os.environ["CHAT_ID"]

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info("VK бот с DialogFlow запущен...")

    send_telegram_from_vk("✅ <b>VK Bot запущен</b>", bot_token_tg, chat_id)

    for event in longpoll.listen():
        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue

        try:
            handle_vk_message(
                vk=vk,
                user_id=event.user_id,
                user_message=event.text,
                dialogflow_project_id=dialogflow_project_id,
                bot_token_tg=bot_token_tg,
                chat_id=chat_id
            )
        except Exception:
            logger.exception("Ошибка обработки сообщения VK:")
            try:
                send_telegram_from_vk("⚠️ <b>VK Bot Error</b>\n\nОшибка обработки сообщения",
                                      bot_token_tg, chat_id)
            except Exception:
                logger.exception("Не удалось отправить сообщение об ошибке:")


if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        logger.error(f"Отсутствует обязательная переменная окружения: {e}")
        raise
    except Exception:
        logger.exception("Critical error in VK bot:")
        raise