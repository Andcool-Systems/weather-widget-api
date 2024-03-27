from json import load as json_encode_file
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from pytz import timezone as pytz_tz


class DefaultTheme:
    def __init__(self, weather_object, language: str, timezone):
        self.timezone = timezone
        self.supported_language = ["ru", "en"]
        self.weather = weather_object
        self.language = language

    def image(self) -> Image:
        # Load language from config
        with open("themes/default/lang.json", "r", encoding="utf-8") as file:
            lang = json_encode_file(file)

        # Load fonts and image
        fnt_big = ImageFont.truetype("themes/default/manrope-bold.ttf", 25)
        fnt_med = ImageFont.truetype("themes/default/manrope-bold.ttf", 15)
        fnt_small = ImageFont.truetype("themes/default/manrope-bold.ttf", 13)
        fnt_med_small = ImageFont.truetype("themes/default/manrope-bold.ttf", 11)
        fnt_very_small = ImageFont.truetype("themes/default/manrope-bold.ttf", 7)
        windArrow = Image.open("themes/default/wind.png")

        # Adaptive timezone
        timezoneList = list(self.timezone)
        timezoneListPreview = timezoneList.copy()
        if timezoneList[3] == "-":
            timezoneList[3] = "+"
        else:
            timezoneList.insert(3, "-")
            timezoneListPreview.insert(3, "+")
        newTimezone = "".join(timezoneList)
        newTimezonePreview = "".join(timezoneListPreview)

        nowTime = datetime.now(pytz_tz(f"Etc/{newTimezone}"))

        # Get weather data
        tempDict = self.weather.temperature("celsius")
        temp = tempDict["temp"]
        feelsLikeTemp = tempDict["feels_like"]

        wind = self.weather.wind()
        windSpeed = wind["speed"]
        windDirection = wind["deg"]
        windStr = lang["wind_dir"][self.language][round(windDirection / 45)]
        humidity = self.weather.humidity
        detailedStatus = self.weather.detailed_status
        pressure = self.weather.pressure["press"]
        visibilityDistance = self.weather.visibility_distance

        # Formatting time
        timeFormatted = f"{lang['at_the_moment'][self.language]} {nowTime.hour}:{nowTime.minute if nowTime.minute > 9 else '0' + str(nowTime.minute)} UTC{newTimezonePreview[-2:]}"

        # Get icon
        icon_name = self.weather.weather_icon_url(size="2x").split("/")[-1]
        weatherIcon = Image.open(f"themes/default/icons/{icon_name}").resize((90, 90))

        # Specify dimensions
        width, height = 345, 145

        # Load image
        mainImage = Image.open("themes/default/background.png")
        mainImage.paste(
            weatherIcon, (0, height // 2 - 90 // 2), weatherIcon
        )  # Paste weather icon to canvas
        line = Image.open("themes/default/line.png")
        draw = ImageDraw.Draw(mainImage)

        # Create temperature string and get size
        temp = f"{round(temp)}°C"
        tempWidth = fnt_big.getbbox(text=temp)[2]
        tempHeight = fnt_big.getbbox(text=temp)[3]

        # Create feels like string and get size
        feelsLike = f"fl: {round(feelsLikeTemp)}°C"
        feelsLikeWidth = fnt_med.getbbox(text=feelsLike)[2]
        feelsLikeHeight = fnt_med.getbbox(text=feelsLike)[3]

        # Paste temperature and feels like to canvas
        draw.text(
            (85, height // 2 - (tempHeight + feelsLikeHeight) // 2),
            temp,
            font=fnt_big,
            fill=(255, 255, 255, 255),
        )
        draw.text(
            (85, (height // 2 - (tempHeight + feelsLikeHeight) // 2) + tempHeight),
            feelsLike,
            font=fnt_med,
            fill=(200, 200, 200, 255),
        )

        mainImage.paste(
            line,
            (max(tempWidth, feelsLikeWidth) + 85 + 15, height // 2 - 128 // 2),
            line,
        )

        offset = (
            max(tempWidth, feelsLikeWidth) + 85 + 15 + 2
        )  # calculate vertical line offset

        # Rotate and paste wind arrow
        arrowRotated = windArrow.rotate(180 - windDirection, resample=Image.BILINEAR)
        mainImage.paste(arrowRotated, (offset + 10, 15), arrowRotated)

        # Create and paste some weather information
        # Paste wind speed text
        draw.text(
            (offset + 30, 16),
            f"{round(windSpeed, 1)}m/s {windStr}",
            font=fnt_small,
            fill=(255, 255, 255, 255),
        )

        # Paste pressure information
        draw.text(
            (offset + 10, 35),
            f"{round(pressure / 1.333, 1)} {lang['pressure'][self.language]}",
            font=fnt_small,
            fill=(255, 255, 255, 255),
        )

        # Paste humidity information
        draw.text(
            (offset + 10, 55),
            f"{lang['humidity'][self.language]}: {humidity}%",
            font=fnt_small,
            fill=(255, 255, 255, 255),
        )

        # Paste visibility information
        draw.text(
            (offset + 10, 75),
            f"{lang['visibility'][self.language]}: {round(visibilityDistance / 1000, 1)}{lang['visibility_range'][self.language]}",
            font=fnt_small,
            fill=(255, 255, 255, 255),
        )
        draw.text(
            (7, height - 13),
            "by AndcoolSystems",
            font=fnt_very_small,
            fill=(180, 180, 180, 255),
        )  # Draw created by line

        detailedStatusText = (
            detailedStatus.capitalize()
        )  # Capialize detailed weather status
        sizeCounter = 15
        detailedStatusFont = ImageFont.truetype(
            "themes/default/manrope-bold.ttf", sizeCounter
        )

        # Calculate detailed weather status font size
        while detailedStatusFont.getbbox(text=detailedStatusText)[2] > (width - 10) - (
            offset + 10
        ):
            detailedStatusFont = ImageFont.truetype(
                "themes/default/manrope-bold.ttf", sizeCounter
            )
            sizeCounter -= 0.5

        # Draw detailed weather status and current time to canvas
        draw.text(
            (offset + 10, 95),
            detailedStatusText,
            font=detailedStatusFont,
            fill=(255, 255, 255, 255),
        )
        draw.text(
            (offset + 10, 115),
            timeFormatted,
            font=fnt_med_small,
            fill=(200, 200, 200, 255),
        )
        return mainImage
