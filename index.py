from uuid import uuid4
from json import dumps as json_encode
from io import BytesIO
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from pytz.exceptions import UnknownTimeZoneError
from pyowm.weatherapi25 import weather as wthr
from themes.default.default import DefaultTheme
from themes.pixel_city.city import PixelCityTheme
from traceback import print_exception
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import uvicorn
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(  # Disable CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
@limiter.limit("30/minute")
async def handler(
    request: Request,
    place: str = "",
    timezone: str = "",
    language: str = "",
    theme: str = "",
    size: str = "",
    json: bool = False
):
    if not place:
        return {
            "statusCode": 400,
            "body": {"status": "error", "message": "`place` query parameter not found"},
        }

    match place:
        case "nightcity":
            location = "perm"  # Easter egg
        case "andcool":
            location = "pskov"
        case _:
            location = place

    timezone = "GMT0" if not timezone else timezone
    language = "ru" if not language else language
    theme = "default" if not theme else theme
    theme_size = "small" if not size else size

    try:
        # Устанавливаем язык
        config_dict = get_default_config()
        config_dict["language"] = language

        # Создаём всякую фигню и объект погоды
        owm = OWM(os.getenv('TOKEN'), config_dict)
        mgr = owm.weather_manager()

        observate = mgr.weather_at_place(location)
        weather: wthr.Weather = observate.weather

        if json:
            return JSONResponse({
                'status': 'success',
                'message': '',
                'temp': weather.temperature("celsius")['temp'],
                'feels_like': weather.temperature("celsius")['feels_like'],
                'pressure': weather.pressure['press'],
                'visibility': weather.visibility_distance,
                'humidity': weather.humidity,
                'wind': weather.wind(),
                'condition': weather.detailed_status.capitalize(),
                'icon': weather.weather_icon_name[:2]
                }, status_code=200)

        # Создаём объект темы
        match theme:
            case "default":
                theme = DefaultTheme(weather, language, timezone)
            case "pixel-city":
                theme = PixelCityTheme(weather, language, theme_size)
            case _:
                return JSONResponse(
                    content={
                        "status": "error",
                        "code": "theme_not_found",
                        "message": f"Theme '{language}' not found."
                        f"Check out the available themes on the repository page on GitHub: "
                        f"https://github.com/Andcool-Systems/weather-widget-api",
                    },
                    status_code=400,
                )

        if language not in theme.supported_language:
            return JSONResponse(
                content={
                    "status": "error",
                    "code": "lang_not_found",
                    "message": f"Language '{language}' not found. Use {', '.join(theme.supported_language)}",
                },
                status_code=400,
            )

        image = theme.image()
    except NotFoundError:
        return {
            "statusCode": 400,
            "body": {
                "status": "error",
                "code": "place_not_found",
                "message": f"Place '{location}' not found.",
            },
        }
    except UnknownTimeZoneError:
        return JSONResponse(
            content={
                "status": "error",
                "code": "tz_not_found",
                "message": f"Timezone '{timezone}' not found. Use gmt(a number between -14 and 12)",
            },
            status_code=400,
        )
    except Exception as e:
        code = str(uuid4())
        print(json_encode({"message": {"uuid": code, "msg": str(e)}, "level": "ERROR"}))
        print_exception(e)

        return JSONResponse(
            content={
                "status": "error",
                "code": "internal_error",
                "message": "internal server error",
                "error_uuid": code,
            },
            status_code=500,
        )

    # Преобразовываем изображение в байты
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")

    # Получаем байты из объекта BytesIO
    image_bytes = image_bytes.getvalue()

    # Кодируем байты изображения в base64
    # encoded_image = b64encode(image_bytes).decode('utf-8')

    # Формируем ответ в виде словаря
    return Response(
        content=image_bytes,
        headers={"Cache-Control": "no-cache", "Age": "0"},
        media_type="image/png",
    )


if __name__ == "__main__":  # Start program
    uvicorn.run("index:app", port=8080, host="0.0.0.0")
