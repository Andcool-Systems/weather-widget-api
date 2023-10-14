from uuid import uuid4
from json import dumps as json_encode
from base64 import b64encode
from io import BytesIO
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pytz.exceptions import UnknownTimeZoneError
from themes.default.default import DefaultTheme


def handler(event, context):
    parameters = event['queryStringParameters']
    if 'place' not in parameters:
        return {"statusCode": 400, "body": {"status": "error", "message": "`place` query parameter not found"}}

    match parameters['place']:
        case 'nightcity':
            location = 'perm'  # Easter egg
        case 'andcool':
            location = 'pskov'
        case _:
            location = parameters['place']

    timezone = "GMT0" if 'timezone' not in parameters else parameters['timezone']
    language = 'ru' if 'language' not in parameters else parameters['language']

    try:
        # Устанавливаем язык
        config_dict = get_default_config()
        config_dict['language'] = language

        # Создаём всякую фигню и объект погоды
        owm = OWM('61d202e168925f843260a7f646f65118', config_dict)
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
    except UnknownTimeZoneError:
        return {
            "statusCode": 400,
            "body": {
                "status": "error",
                "code": "tz_not_found",
                "message": f"Timezone '{timezone}' not found. Use gmt(a number between -14 and 12)"
            }
        }
    except Exception as e:
        code = str(uuid4())
        print(json_encode({'message': {'uuid': code, 'msg': str(e)}, 'level': 'ERROR'}))

        return {
            "statusCode": 500,
            "body": {
                "status": "error",
                "code": "internal_error",
                "message": "internal server error",
                "error_uuid": code
            }
        }

    # Преобразовываем изображение в байты
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')

    # Получаем байты из объекта BytesIO
    image_bytes = image_bytes.getvalue()

    # Кодируем байты изображения в base64
    encoded_image = b64encode(image_bytes).decode('utf-8')

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
