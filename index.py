from uuid import uuid4
from json import dumps as json_encode
from base64 import b64encode
from io import BytesIO
from os import environ
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from pytz.exceptions import UnknownTimeZoneError
from themes.default.default import DefaultTheme
from themes.pixel_city.city import PixelCityTheme
from traceback import print_exception


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
    theme = 'default' if 'theme' not in parameters else parameters['theme']
    theme_size = 'small' if 'size' not in parameters else parameters['size']

    try:
        # Устанавливаем язык
        config_dict = get_default_config()
        config_dict['language'] = language

        # Создаём всякую фигню и объект погоды
        owm = OWM(environ['OWM_TOKEN'], config_dict)
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(location)
        weather = observation.weather

        # Создаём объект темы
        match theme:
            case 'default':
                theme = DefaultTheme(weather, language, timezone)
            case 'pixel-city':
                theme = PixelCityTheme(weather, language, theme_size)
            case _:
                return {
                    "statusCode": 400,
                    "body": {
                        "status": "error",
                        "code": "theme_not_found",
                        "message": f"Theme '{language}' not found."
                                   f"Check out the available themes on the repository page on GitHub: "
                                   f"https://github.com/Andcool-Systems/weather-widget-api"
                    }
                }

        if language not in theme.supported_language:
            return {
                "statusCode": 400,
                "body": {
                    "status": "error",
                    "code": "lang_not_found",
                    "message": f"Language '{language}' not found. Use {', '.join(theme.supported_language)}"
                }
            }

        image = theme.image()
    except NotFoundError:
        return {
            "statusCode": 400,
            "body": {
                "status": "error",
                "code": "place_not_found",
                "message": f"Place '{location}' not found."
            }
        }
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
        code = str(uuid4())  # Some code
        print(json_encode({'message': {'uuid': code, 'msg': str(e)}, 'level': 'ERROR'}))
        print_exception(e)

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
