from PIL import Image, ImageFont, ImageDraw
from pyowm.weatherapi25 import weather as wthr


class PixelCityTheme:
    def __init__(self, weather_object: wthr.Weather, language: str, theme_size: str):
        self.supported_language = ['ru', 'en']  # TODO: add jp
        self.theme_size = theme_size
        self.weather = weather_object
        self.language = language

    def image(self) -> Image:
        # Импортируем все необходимое
        if self.theme_size == 'big':
            poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 128)
            montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", 64)
            opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", 48)
        else:
            poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 64)
            montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", 32)
            opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", 24)

        # Получаем данные о погоде
        temperature_info = self.weather.temperature('celsius')
        temperature, temperature_fl = round(temperature_info['temp']), round(temperature_info['feels_like'])
        details = self.weather.detailed_status.capitalize()
        humidity = self.weather.humidity
        visibility_distance = round(self.weather.visibility_distance / 1000)

        # Импортируем фон
        match self.weather.weather_icon_name:
            case '01d':
                background_name = 'day'
            case '01n':
                background_name = 'night'
            case '02d':
                background_name = 'day_few_clouds'
            case '02n':
                background_name = 'night_few_clouds'
            case '03d':
                background_name = 'day_few_clouds'
            case '03n':
                background_name = 'night_few_clouds'
            case '04d' | '04n':
                background_name = 'broken_clouds'
            case '09d' | '09n':
                background_name = 'shower_rain'
            case '10d':
                background_name = 'day_rain'
            case '10n':
                background_name = 'night_rain'
            case '11d' | '11n':
                background_name = 'thunderstorm'
            case '13d' | '13n':
                background_name = 'snow'
            case '50n':
                background_name = 'mist'

        if self.theme_size == 'big':
            source = Image.open(f'themes/pixel_city/backgrounds/big/{background_name}.png')
        else:
            source = Image.open(f'themes/pixel_city/backgrounds/small/{background_name}.png')

        draw = ImageDraw.Draw(source)

        # Создаём текста
        text_temperature = f'{temperature}°C'

        match self.language:
            case 'en':
                other_info = f'fl: {temperature_fl}°C / H: {humidity}% / V: {visibility_distance} km'
            case 'ru':
                other_info = f'fl: {temperature_fl}°C / H: {humidity}% / V: {visibility_distance} км'

        # Рисуем
        # Создаём текст температуры
        temp_data = poppins.getbbox(text=text_temperature)

        if self.theme_size == 'big':
            for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((1024 / 2 + i[0] - temp_data[2] / 2, 216 + i[1]), text_temperature, font=poppins, fill=(0, 0, 0, 100))

            draw.text((1024 / 2 - temp_data[2] / 2, 216), text_temperature, font=poppins, fill=(255, 255, 255, 255))

            # Создаём текст деталей погоды
            details_data = montserrat.getbbox(text=details)

            for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((1024 / 2 + i[0] - details_data[2] / 2, 357 + i[1]), details, font=montserrat, fill=(0, 0, 0, 100))

            draw.text((1024 / 2 - details_data[2] / 2, 357), details, font=montserrat, fill=(250, 250, 250, 255))

            # Создаём текст прочей информации о погоде
            other_data = opensans.getbbox(text=other_info)

            for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((1024 / 2 + i[0] - other_data[2] / 2, 435 + i[1]), other_info, font=opensans, fill=(0, 0, 0, 100))

            draw.text((1024 / 2 - other_data[2] / 2, 435), other_info, font=opensans, fill=(246, 245, 245, 255))
        else:
            for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((512 / 2 + i[0] - temp_data[2] / 2, 108 + i[1]), text_temperature, font=poppins,
                          fill=(0, 0, 0, 100))

            draw.text((512 / 2 - temp_data[2] / 2, 108), text_temperature, font=poppins, fill=(255, 255, 255, 255))

            # Создаём текст деталей погоды
            details_data = montserrat.getbbox(text=details)

            for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((512 / 2 + i[0] - details_data[2] / 2, 178 + i[1]), details, font=montserrat,
                          fill=(0, 0, 0, 100))

            draw.text((512 / 2 - details_data[2] / 2, 178), details, font=montserrat, fill=(250, 250, 250, 255))

            # Создаём текст прочей информации о погоде
            other_data = opensans.getbbox(text=other_info)

            for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((512 / 2 + i[0] - other_data[2] / 2, 217 + i[1]), other_info, font=opensans,
                          fill=(0, 0, 0, 100))

            draw.text((512 / 2 - other_data[2] / 2, 217), other_info, font=opensans, fill=(246, 245, 245, 255))

        return source
