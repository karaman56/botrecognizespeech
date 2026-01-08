import logging
from google.cloud import dialogflow_v2beta1 as dialogflow

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

        return response

    except Exception as e:
        error_msg = f"DialogFlow error: {e}"
        logger.error(error_msg)
        return None