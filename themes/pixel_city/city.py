from json import load as json_encode_file
from PIL import Image, ImageFont, ImageDraw


class PixelCityTheme:
    def __init__(self, weather_object, language: str):
        self.supported_language = ['ru', 'en']  # TODO: add jp
        self.weather = weather_object
        self.language = language

    def image(self) -> Image:
        # Импортируем все необходимое
        poppins = ImageFont.truetype("Poppins-SemiBold.ttf", 128)
        montserrat = ImageFont.truetype("Montserrat-Medium.ttf", 64)
        opensans = ImageFont.truetype("OpenSans-SemiBold.ttf", 48)

        # Получаем данные о погоде
        temperature_info = self.weather.temperature('celsius')
        temperature, temperature_fl = temperature_info['temp'], temperature_info['feels_like']
        details = self.weather.detailed_status
        humidity = self.weather.humidity
        visibility_distance = round(self.weather.visibility_distance / 1000)
        icon_name = self.weather.weather_icon_url().split('/')[-1]

        # Импортируем фон
        match icon_name:
            case '01d.png':
                background_name = 'day'
            case '01n.png':
                background_name = 'night'
            case '02d.png':
                background_name = 'day_few_clouds'
            case '02n.png':
                background_name = 'night_few_clouds'
            case '03d.png':
                background_name = 'day_few_clouds'
            case '03n.png':
                background_name = 'night_few_clouds'
            case '04d.png' | '04n.png':
                background_name = 'broken_clouds'
            case '09d.png' | '09n.png':
                background_name = 'shower_rain'
            case '10d.png':
                background_name = 'day_rain'
            case '10n.png':
                background_name = 'night_rain'
            case '11d.png' | '11n.png':
                background_name = 'thunderstorm'
            case '13d.png' | '13n.png':
                background_name = 'snow'
            case '50n.png':
                background_name = 'mist'

        source = Image.open(f'themes/pixel_city/backgrounds/{background_name}.png')
        draw = ImageDraw.Draw(source)

        # Создаём текста
        text_temperature = f'{temperature}°C'

        match self.language:
            case 'en':
                other_info = f'fl: {temperature_fl}°C / H: {humidity}% | V: {visibility_distance} km'
            case 'ru':
                other_info = f'fl: {temperature_fl}°C / H: {humidity}% | V: {visibility_distance} км'

        # Рисуем
        # Создаём текст температуры
        temp_data = poppins.getbbox(text=text_temperature)

        for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            draw.text((1024 / 2 + i[0] - temp_data[2] / 2, 216 + i[1]), text_temperature, font=poppins, fill=(0, 0, 0, 1))

        draw.text((1024 / 2 - temp_data[2] / 2, 216), text_temperature, font=poppins, fill=(255, 255, 255, 255))

        # Создаём текст деталей погоды
        details_data = montserrat.getbbox(text=details)

        for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            draw.text((1024 / 2 + i[0] - details_data[2] / 2, 357 + i[1]), details, font=montserrat, fill=(0, 0, 0, 1))

        draw.text((1024 / 2 - details_data[2] / 2, 357), details, font=montserrat, fill=(250, 250, 250, 255))

        # Создаём текст прочей информации о погоде
        other_data = opensans.getbbox(text=other_info)

        for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            draw.text((1024 / 2 + i[0] - other_data[2] / 2, 435 + i[1]), other_info, font=opensans, fill=(0, 0, 0, 1))

        draw.text((1024 / 2 - other_data[2] / 2, 435), other_info, font=opensans, fill=(246, 245, 245, 255))


