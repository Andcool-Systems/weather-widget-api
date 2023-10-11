import json
import uuid

from themes.default.default import DefaultTheme
import base64
from io import BytesIO
import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils.config import get_default_config
import pytz


def handler(event, context):
    parameters = event['queryStringParameters']
    if 'place' not in parameters:
        return {"statusCode": 400, "body": {"status": "error", "message": "`place` query parameter not found"}}

    if parameters['place'] == 'nightcity':
        # Если ты нашёл эту фичу - молодец. Теперь ты знаешь что такое nightcity на самом деле.
        location = 'perm'
        location = 'perm'
    elif parameters['place'] == 'andcool':
        location = 'pskov'
        location = 'pskov'
    else:
        location = parameters["place"]
        location = parameters["place"]

    timezone = "GMT0" if 'timezone' not in parameters else parameters['timezone']
    language = 'ru' if 'language' not in parameters else parameters['language']
    try:
        # Устанавливаем язык
        config_dict = get_default_config()
        config_dict['language'] = language

        # Создаём всякую фигню и объект погоды
        owm = pyowm.OWM('61d202e168925f843260a7f646f65118', config_dict)
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(location)
        weather = observation.weather
        # Создаём объект темы
        theme = DefaultTheme(weather, language, timezone)

        if language not in theme.supported_language:
            return {
                "statusCode": 400,
                "body": {
                    "status": "error",
                    "code": "lang_not_found",
                    "message": f"Language '{language}' not found. Use `ru` or `en`"
                }
            }
        image = theme.image()

    except pytz.exceptions.UnknownTimeZoneError:
        return {
            "statusCode": 400,
            "body": {
                "status": "error",
                "code": "tz_not_found",
                "message": f"Timezone '{timezone}' not found. Use gmt(a number between -14 and 12)"
            }
        }
    except Exception as e:
        uid = str(uuid.uuid4())
        print(json.dumps({'message': {'uuid': uid, 'msg': str(e)}, 'level': 'ERROR'}))

        return {
            "statusCode": 500,
            "body": {
                "status": "error",
                "code": "internal_error",
                "message": "internal server error",
                "error_uuid": uid
            }
        }

    # Преобразовываем изображение в байты
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')

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
