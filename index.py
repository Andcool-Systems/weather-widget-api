import json
import pyowm
from pyowm.utils.config import get_default_config
from PIL import Image, ImageDraw, ImageFont
import base64
import requests
from io import BytesIO
from datetime import datetime
import pytz

config_dict = get_default_config()
config_dict['language'] = 'ru'
wind_r = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
fnt_big = ImageFont.truetype("manrope-bold.ttf", 25)
fnt_med = ImageFont.truetype("manrope-bold.ttf", 15)
fnt_small = ImageFont.truetype("manrope-bold.ttf", 13)
fnt_med_small = ImageFont.truetype("manrope-bold.ttf", 11)
fnt_very_small = ImageFont.truetype("manrope-bold.ttf", 7)
windArrow = Image.open("wind.png")


def get_weather(place, timezone):
    owm = pyowm.OWM('61d202e168925f843260a7f646f65118', config_dict)
    mgr = owm.weather_manager()
    timezoneList = list(timezone)
    timezoneListPreview = timezoneList.copy()
    if timezoneList[3] == "-": timezoneList[3] = "+"
    else: 
        timezoneList.insert(3, "-")
        timezoneListPreview.insert(3, "+")
    newTimezone = "".join(timezoneList)
    newTimezonePreview = "".join(timezoneListPreview)
    nowTime = datetime.now(pytz.timezone(f"Etc/{newTimezone}"))

    #try:
    if True:
        observation = mgr.weather_at_place(place)
        w = observation.weather

        tempDict = w.temperature("celsius")
        temp = tempDict['temp']
        feelsLikeTemp = tempDict['feels_like']
        windSpeed = w.wind()['speed']
        windDirection = w.wind()['deg']
        windStr = wind_r[round((windDirection) / 45)]
        humidity = w.humidity
        detailedStatus = w.detailed_status
        pressure = w.pressure['press']
        visibilityDistance = w.visibility_distance
        timeFormatted = f"На момент {nowTime.hour}:{nowTime.minute if nowTime.minute > 9 else '0' + str(nowTime.minute)} UTC{newTimezonePreview[-2:]}"

        response = requests.get(w.weather_icon_url(size='2x'))
        weatherIcon = Image.open(BytesIO(response.content)).resize((90, 90))
        
        width = 345
        height = 145

        mainImage = Image.open("background.png")
        mainImage.paste(weatherIcon, (0, height // 2 - 90 // 2), weatherIcon)
        line = Image.open("line.png")
        draw = ImageDraw.Draw(mainImage)

        temp = f"{round(temp)}°C"
        tempWidth = fnt_big.getbbox(text=temp)[2]
        tempHeight = fnt_big.getbbox(text=temp)[3]
        
        feelsLike = f"fl: {round(feelsLikeTemp)}°C"
        feelsLikeWidth = fnt_med.getbbox(text=feelsLike)[2]
        feelsLikeHeight = fnt_med.getbbox(text=feelsLike)[3]

        draw.text((85, height // 2 - (tempHeight + feelsLikeHeight) // 2), temp, font=fnt_big, fill=(255, 255, 255, 255))
        draw.text((85, (height // 2 - (tempHeight + feelsLikeHeight) // 2) + tempHeight), feelsLike, font=fnt_med, fill=(200, 200, 200, 255))

        mainImage.paste(line, (max(tempWidth, feelsLikeWidth) + 85 + 15, height // 2 - 128 // 2), line)

        offset = max(tempWidth, feelsLikeWidth) + 85 + 15 + 2
        arrowRotated = windArrow.rotate(180 - windDirection, resample=Image.BILINEAR)
        mainImage.paste(arrowRotated, (offset + 10, 15), arrowRotated)

        draw.text((offset + 30, 16), f"{round(windSpeed, 1)}m/s {windStr}", font=fnt_small, fill=(255, 255, 255, 255))
        draw.text((offset + 10, 35), f"{round(pressure / 1.333, 1)} мм рт. ст.", font=fnt_small, fill=(255, 255, 255, 255))
        draw.text((offset + 10, 55), f"Влажность: {humidity}%", font=fnt_small, fill=(255, 255, 255, 255))
        draw.text((offset + 10, 75), f"Видимость: {round(visibilityDistance / 1000, 1)}км", font=fnt_small, fill=(255, 255, 255, 255))
        draw.text((7, height - 13), "by AndcoolSystems", font=fnt_very_small, fill=(180, 180, 180, 255))
        
        detailedStatusText = detailedStatus.capitalize()
        sizeCounter = 15
        detailedStatusFont = ImageFont.truetype("manrope-bold.ttf", sizeCounter)
        while detailedStatusFont.getbbox(text=detailedStatusText)[2] > (width - 10) - (offset + 10):
            detailedStatusFont = ImageFont.truetype("manrope-bold.ttf", sizeCounter)
            sizeCounter -= 0.5
        draw.text((offset + 10, 95), detailedStatusText, font=detailedStatusFont, fill=(255, 255, 255, 255))
        draw.text((offset + 10, 115), timeFormatted, font=fnt_med_small, fill=(200, 200, 200, 255))
        return mainImage
    #except Exception as e:
        #print(e)


def landing():
    with open('page.html', mode='r') as file:
        body = file.read()

    return {"statusCode": 200, "headers": {"Content-type": "text/html; charset=UTF-8"}, "body": body}


def handler(event, context):
    if not event['queryStringParameters']:
        return landing()
    
    if 'place' not in event['queryStringParameters']:
        return {"statusCode": 400,
                "body": {"status": "error", "message": "place query parameter not found"}}
    if event['queryStringParameters']['place'] == 'nightcity':
        # Если ты нашёл эту фичу - молодец. Теперь ты знаешь что такое nightcity на самом деле.
        city = 'perm'
    elif event['queryStringParameters']['place'] == 'andcool':
        city = 'pskov'
    else:
        city = event["queryStringParameters"]["place"]
    
    if 'timezone' not in event['queryStringParameters']: 
        timezone = "GMT0"
    else: 
        timezone = event['queryStringParameters']['timezone']

    image = get_weather(city, timezone)
    
    if image == None: return {
        "statusCode": 500,
        "body": {"status": "error", "message": "internal server error"}
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
    
