from PIL import Image
from pyowm.weatherapi25.weather import Weather


class BaseTheme:
    def __init__(self, weather_object: Weather, language: str):
        self.weather = weather_object
        self.language = language
        self.supported_language = []

    @property
    def image(self) -> Image:
        raise 'It\'s base class. Use this only as an abstraction for creating new classes.'
