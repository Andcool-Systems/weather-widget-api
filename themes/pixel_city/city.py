from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont


class PixelCityTheme:
    def __init__(self, weather_object, language: str, theme_size: str):
        self.supported_language = ['ru', 'en', 'it', 'es', 'sp', 'ua', 'uk', 'de', 'pt', 'ro', 'pl', 'fi', 'nl', 'fr',
                                   'bg', 'sv', 'se', 'zh_tw', 'zh', 'zh_cn', 'tr', 'hr', 'ca']
        self.theme_size = theme_size
        self.weather = weather_object
        self.language = language

    def draw_text(self, draw: ImageDraw, font: FreeTypeFont, text: str, y_coordinate: int):
        text_data = font.getbbox(text=text)
        width = 1024 if self.theme_size == 'big' else 512

        for i in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            draw.text((width / 2 + i[0] - text_data[2] / 2, y_coordinate + i[1]), text, font=font, fill=(0, 0, 0, 128))

        draw.text((width / 2 - text_data[2] / 2, y_coordinate), text, font=font, fill=(255, 255, 255, 255))

    def open_fonts(self) -> [FreeTypeFont, FreeTypeFont, FreeTypeFont]:
        font_size = (128, 64, 48) if self.theme_size == 'big' else (64, 32, 24)

        poppins = ImageFont.truetype("themes/pixel_city/Poppins-SemiBold.ttf", font_size[0])

        if self.language == 'zh_tw':
            montserrat = ImageFont.truetype('themes/pixel_city/NotoSansTC-Medium.ttf', font_size[1])
            opensans = ImageFont.truetype("themes/pixel_city/NotoSansTC-SemiBold.ttf", font_size[2])
        elif self.language == 'zh' or self.language == 'zh_cn':
            montserrat = ImageFont.truetype('themes/pixel_city/NotoSansSC-Medium.ttf', font_size[1])
            opensans = ImageFont.truetype("themes/pixel_city/NotoSansSC-SemiBold.ttf", font_size[2])
        else:
            montserrat = ImageFont.truetype("themes/pixel_city/Montserrat-Medium.ttf", font_size[1])
            opensans = ImageFont.truetype("themes/pixel_city/OpenSans-SemiBold.ttf", font_size[2])

        return poppins, montserrat, opensans

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
        icon_to_background = {
            '01d.png': 'day',
            '01n.png': 'night',
            '02d.png': 'day_few_clouds',
            '02n.png': 'night_few_clouds',
            '03d.png': 'day_few_clouds',
            '03n.png': 'night_few_clouds',
            '04d.png': 'broken_clouds',
            '04n.png': 'broken_clouds',
            '09d.png': 'shower_rain',
            '09n.png': 'shower_rain',
            '10d.png': 'day_rain',
            '10n.png': 'night_rain',
            '11d.png': 'thunderstorm',
            '11n.png': 'thunderstorm',
            '13d.png': 'snow',
            '13n.png': 'snow',
            '50n.png': 'mist',
            '50d.png': 'mist'
        }

        background_name = icon_to_background.get(icon_name, "day")

        source = Image.open(f'themes/pixel_city/backgrounds/{self.theme_size}/{background_name}.png')
        draw = ImageDraw.Draw(source)

        # Создаём текста
        text_temperature = f'{temperature}°C'
        poppins, montserrat, opensans = self.open_fonts()

        match self.language:
            case 'ru' | 'ua' | 'uk':
                other_info = f'fl: {temperature_fl}°C / H: {humidity}% / V: {visibility_distance} км'
            case 'zh_tw':
                other_info = f'感覺像: {temperature_fl}°C / 濕度: {humidity}% / 能見度: {visibility_distance} 公里'
            case 'zh' | 'zh_cn':
                other_info = f'感觉像: {temperature_fl}°C / 湿度: {humidity}% / 能见度: {visibility_distance} 公里'
            case _:
                other_info = f'fl: {temperature_fl}°C / H: {humidity}% / V: {visibility_distance} km'

        self.draw_text(draw, poppins, text_temperature, 216 if self.theme_size == 'big' else 108)
        self.draw_text(draw, montserrat, details, 357 if self.theme_size == 'big' else 178)
        self.draw_text(draw, opensans, other_info, 435 if self.theme_size == 'big' else 217)

        return source
