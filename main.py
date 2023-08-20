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
fnt = ImageFont.truetype("manrope-bold.ttf", 25)
fnts = ImageFont.truetype("manrope-bold.ttf", 20)
fntss = ImageFont.truetype("manrope-bold.ttf", 15)
fntsss = ImageFont.truetype("manrope-bold.ttf", 13)
fntssss = ImageFont.truetype("manrope-bold.ttf", 7)
arrow = Image.open("wind.png")


def getWeather(place):
    owm = pyowm.OWM('61d202e168925f843260a7f646f65118', config_dict)
    mgr = owm.weather_manager()
    try:
    #if True:
        observation = mgr.weather_at_place(place)
        w = observation.weather

        t = w.temperature("celsius")
        t1 = t['temp']
        t2 = t['feels_like']
        wi_s = w.wind()['speed']
        wi_d = w.wind()['deg']
        wind_ru = wind_r[round((wi_d) / 45)]
        humi = w.humidity
        dt = w.detailed_status
        pr = w.pressure['press']
        vd = w.visibility_distance

        response = requests.get(w.weather_icon_url(size='2x'))
        imgIcon = Image.open(BytesIO(response.content)).resize((90, 90))
        
        width = 345
        height = 145

        mainImage = Image.open("background.png")
        mainImage.paste(imgIcon, (0, height // 2 - 90 // 2), imgIcon)
        line = Image.open("line.png")
        
        d = ImageDraw.Draw(mainImage)
        temp = f"{round(t1)}°C"
        tw = fnt.getbbox(text=temp)[2]
        th = fnt.getbbox(text=temp)[3]
        
        feelsLike = f"fl: {round(t2)}°C"
        twf = fntss.getbbox(text=feelsLike)[2]
        thf = fntss.getbbox(text=feelsLike)[3]

        d.text((85, height // 2 - (th + thf) // 2), temp, font=fnt, fill=(255, 255, 255, 255))
        d.text((85, (height // 2 - (th + thf) // 2) + th), feelsLike, font=fntss, fill=(200, 200, 200, 255))

        mainImage.paste(line, (max(tw, twf) + 85 + 15, height // 2 - 128 // 2), line)

        xPos = max(tw, twf) + 85 + 15 + 2
        arrowRot = arrow.rotate(180 - wi_d, resample=Image.BILINEAR)
        mainImage.paste(arrowRot, (xPos + 10, 15), arrowRot)

        d.text((xPos + 30, 16), f"{round(wi_s, 1)}m/s {wind_ru}", font=fntsss, fill=(255, 255, 255, 255))
        d.text((xPos + 10, 35), f"{round(pr / 1.333, 1)} мм рт. ст.", font=fntsss, fill=(255, 255, 255, 255))
        d.text((xPos + 10, 55), f"Влажность: {humi}%", font=fntsss, fill=(255, 255, 255, 255))
        d.text((xPos + 10, 75), f"Видимость: {round(vd / 1000, 1)}км", font=fntsss, fill=(255, 255, 255, 255))
        d.text((7, height - 13), "by AndcoolSystems", font=fntssss, fill=(180, 180, 180, 255))
        
        ds = dt.capitalize()
        sizeCounter = 15
        fntch = ImageFont.truetype("manrope-bold.ttf", sizeCounter)

        while fntch.getbbox(text=ds)[2] > (width - 10) - (xPos + 10):
            fntch = ImageFont.truetype("manrope-bold.ttf", sizeCounter)
            sizeCounter -= 0.5
        d.text((xPos + 10, 95), ds, font=fntch, fill=(255, 255, 255, 255))
        
        return mainImage
    except Exception as e:
        print(e)
	

class Quote(Resource):
	@limiter.limit("10/second")
	def get(self, method=None):
		if method == None: return "weather api", 200
		if method == "weather": 
			argsNF = request.args
			args = argsNF.to_dict()

			image = getWeather(args["place"])
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


def run():
    app.run(host='0.0.0.0', port=8080)

run()


