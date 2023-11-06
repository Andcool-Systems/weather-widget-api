from PIL import Image, ImageFont, ImageDraw


class PixelCityTheme:
    def __init__(self, weather_object, language: str, theme_size: str):
        self.supported_language = ['ru', 'en', 'it', 'es', 'sp', 'ua', 'uk', 'de', 'pt', 'ro', 'pl', 'fi', 'nl', 'fr',
                                   'bg', 'sv', 'se', 'zh_tw', 'zh', 'zh_cn', 'tr', 'hr', 'ca']
        self.theme_size = theme_size
        self.weather = weather_object
        self.language = language

    def image(self) -> Image:
        # Получаем данные о погоде
        temperature_info = self.weather.temperature('celsius')
        temperature, temperature_fl = round(temperature_info['temp']), round(temperature_info['feels_like'])
        details = self.weather.detailed_status
        details = details[0].upper() + details[1:]
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
            case '50n.png' | '50d.png':
                background_name = 'mist'

        if self.theme_size == 'big':
            source = Image.open(f'themes/pixel_city/backgrounds/big/{background_name}.png')
        else:
            source = Image.open(f'themes/pixel_city/backgrounds/small/{background_name}.png')

        draw = ImageDraw.Draw(source)

        # Создаём текста
        text_temperature = f'{temperature}°C'

        match self.language:
            case 'ru' | 'ua' | 'uk':
                if self.theme_size == 'big':
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 128)
                    montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", 64)
                    opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", 48)
                else:
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 64)
                    montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", 32)
                    opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", 24)

                other_info = f'fl: {temperature_fl}°C / H: {humidity}% / V: {visibility_distance} км'
            case 'zh_tw':
                if self.theme_size == 'big':
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 128)
                    montserrat = ImageFont.truetype('themes/pixel_city/NotoSansTC-Medium.ttf', 64)
                    opensans = ImageFont.truetype("themes/pixel_city/NotoSansTC-SemiBold.ttf", 48)
                else:
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 64)
                    montserrat = ImageFont.truetype('themes/pixel_city/NotoSansTC-Medium.ttf', 32)
                    opensans = ImageFont.truetype("themes/pixel_city/NotoSansTC-SemiBold.ttf", 24)

                other_info = f'感覺像: {temperature_fl}°C / 濕度: {humidity}% / 能見度: {visibility_distance} 公里'
            case 'zh' | 'zh_cn':
                if self.theme_size == 'big':
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 128)
                    montserrat = ImageFont.truetype('themes/pixel_city/NotoSansSC-Medium.ttf', 64)
                    opensans = ImageFont.truetype("themes/pixel_city/NotoSansSC-SemiBold.ttf", 48)
                else:
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 64)
                    montserrat = ImageFont.truetype('themes/pixel_city/NotoSansSC-Medium.ttf', 32)
                    opensans = ImageFont.truetype("themes/pixel_city/NotoSansSC-SemiBold.ttf", 24)

                other_info = f'感觉像: {temperature_fl}°C / 湿度: {humidity}% / 能见度: {visibility_distance} 公里'
            case _:
                if self.theme_size == 'big':
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 128)
                    montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", 64)
                    opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", 48)
                else:
                    poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", 64)
                    montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", 32)
                    opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", 24)

                other_info = f'fl: {temperature_fl}°C / H: {humidity}% / V: {visibility_distance} km'

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
