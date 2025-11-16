import os
from google.cloud import dialogflow_v2beta1 as dialogflow

# Настройки
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/monster/.config/gcloud/application_default_credentials.json"


def simple_dialogflow_test():
    """Простой тест DialogFlow"""
    project_id = "mybott-turm"
    session_id = "test-session-001"
    message = "Hello"

    try:
        # Создаем клиент
        session_client = dialogflow.SessionsClient()

        # Создаем сессию
        session = session_client.session_path(project_id, session_id)
        print(f"🔄 Session: {session}")

        # Создаем запрос
        text_input = dialogflow.TextInput(text=message, language_code='en')
        query_input = dialogflow.QueryInput(text=text_input)

        # Отправляем запрос
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        # Выводим результат
        print("✅ УСПЕХ! DialogFlow ответил:")
        print(f"💬 Ваш вопрос: {message}")
        print(f"🤖 Ответ бота: {response.query_result.fulfillment_text}")
        print(f"🎯 Интент: {response.query_result.intent.display_name}")
        print(f"📊 Уверенность: {response.query_result.intent_detection_confidence}")

    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        print("\nВозможные проблемы:")
        print("1. Неправильный project_id")
        print("2. DialogFlow API не включен")
        print("3. Нет прав доступа")
        print("4. В агенте нет интентов")


if __name__ == "__main__":
    simple_dialogflow_test()
