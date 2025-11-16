from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
import datetime


def create_api_key(project_id: str, suffix: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response


if __name__ == "__main__":
    # ЗАМЕНИТЕ 'your-project-id' НА ВАШ РЕАЛЬНЫЙ PROJECT_ID
    project_id = "mybott-turm"  # TODO: замените этот ID

    # Создаем уникальный суффикс для ключа
    suffix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Вызываем функцию создания API ключа
    try:
        api_key = create_api_key(project_id, suffix)
        print("\n" + "=" * 50)
        print("API KEY CREATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"Key name: {api_key.name}")
        print(f"Key string: {api_key.key_string}")  # Это ваш API ключ
        print("=" * 50)
    except Exception as e:
        print(f"Error creating API key: {e}")