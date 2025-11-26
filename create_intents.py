import json
import os
from google.cloud import dialogflow_v2beta1 as dialogflow

# Настройки
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/monster/.config/gcloud/application_default_credentials.json"
PROJECT_ID = "mybot-lhba"
LANGUAGE_CODE = "ru"


def create_intent(display_name, training_phrases_parts, message_texts):
    """Создает интент в DialogFlow"""

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(PROJECT_ID)

    # Подготавливаем тренировочные фразы
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    # Подготавливаем ответы
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    # Создаем интент
    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    # Отправляем запрос на создание
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"✅ Создан интент: {display_name}")
    return response


def load_questions_from_json(file_path):
    """Загружает вопросы и ответы из JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"❌ Ошибка загрузки JSON: {e}")
        return None


def main():
    """Основная функция для создания интентов"""

    # Загружаем данные из JSON файла
    json_data = load_questions_from_json('questions.json')

    if not json_data:
        print("Не удалось загрузить данные из JSON файла")
        return

    print("🚀 Начинаем создание интентов...")
    print("=" * 50)

    # Создаем каждый интент
    for intent_name, intent_data in json_data.items():
        questions = intent_data['questions']
        answer = intent_data['answer']

        print(f"📝 Создаем интент: '{intent_name}'")
        print(f"   📋 Фраз: {len(questions)}")
        print(f"   💬 Ответ: {answer[:50]}...")

        try:
            create_intent(
                display_name=intent_name,
                training_phrases_parts=questions,
                message_texts=[answer]
            )
            print(f"   ✅ Успешно создан!\n")

        except Exception as e:
            print(f"   ❌ Ошибка: {e}\n")

    print("=" * 50)
    print("🎉 Все интенты созданы! Проверьте в DialogFlow Console.")


if __name__ == "__main__":
    main()