from flask import Flask, send_file, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from io import BytesIO
import pyowm
from pyowm.utils.config import get_default_config
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app = Flask(__name__)
api = Api(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
notAlowed = {
	"status": "error",
	"message": "The method is not allowed for the requested URL."
    }
    
config_dict = get_default_config()
config_dict['language'] = 'ru'
wind_r = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
fnt_big = ImageFont.truetype("manrope-bold.ttf", 25)
fnt_med = ImageFont.truetype("manrope-bold.ttf", 15)
fnt_small = ImageFont.truetype("manrope-bold.ttf", 13)
fnt_very_small = ImageFont.truetype("manrope-bold.ttf", 7)
windArrow = Image.open("wind.png")


def getWeather(place):
    owm = pyowm.OWM('61d202e168925f843260a7f646f65118', config_dict)
    mgr = owm.weather_manager()
    try:
    #if True:
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
        return mainImage
    except Exception as e:
        print(e)
	

class Quote(Resource):
	@limiter.limit("10/second")
	def get(self, method=None):
		if method == None: return "Weather widget API", 200
		if method == "weather": 
			argsNF = request.args
			args = argsNF.to_dict()

			image = getWeather(args["place"])
			if image == None: return {"status": "error", "message": "internal server error"}, 500
			bio = BytesIO()
			bio.name = f"weather{id}.png"
			image.save(bio, "PNG")
			bio.seek(0)
			return send_file(bio, mimetype='image/png')
		return notAlowed, 405


api.add_resource(Quote, 
                 "/", 
                 "/<string:method>", 
                 "/<string:method>/"
                 )

app.run(host='0.0.0.0', port=8080)




