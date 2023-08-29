import json
import uuid

from weather import Weather
from themes.default.default import DefaultTheme
import base64
from io import BytesIO
import pyowm

with open('lang.json', 'r', encoding="utf-8") as openfile:
    lang = json.load(openfile)


def handler(event, context):
    parameters = event['queryStringParameters']

    if 'place' not in parameters:
        return {"statusCode": 400, "body": {"status": "error", "message": "`place` query parameter not found"}}

    if parameters['place'] == 'nightcity':
        # Если ты нашёл эту фичу - молодец. Теперь ты знаешь что такое nightcity на самом деле.
        city = 'perm'
    elif parameters['place'] == 'andcool':
        city = 'pskov'
    else:
        city = parameters["place"]

    timezone = "GMT0" if 'timezone' not in parameters else parameters['timezone']
    language = 'ru' if 'language' not in parameters else parameters['language']

    try:
        weather = Weather(city, language)
        weather.get_current()
    except pyowm.commons.exceptions.NotFoundError:
        return {
            "statusCode": 404,
            "body": {"status": "error", "message": f"place '{city}' not found"}
        }

    try:
        image = DefaultTheme(weather, language, timezone).image
    except Exception as e:
        uid = str(uuid.uuid4())
        print(uid, e)

        return {
            "statusCode": 500,
            "body": {"status": "error", "message": "internal server error", "error_uuid": uid}
        }

    # Преобразовываем изображение в байты
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')  # Замените 'JPEG' на формат вашего изображения

    # Получаем байты из объекта BytesIO
    image_bytes = image_bytes.getvalue()

    # Кодируем байты изображения в base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    # Формируем ответ в виде словаря
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/png",
            "Cache-Control": "no-cache",
            "Age": 0
        },
        "body": encoded_image,
        "isBase64Encoded": True
    }
    return response
