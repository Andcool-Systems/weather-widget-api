import weather
from PIL import Image


class BaseTheme:
    def __init__(self, weather_object: weather.Weather, language: str):
        self.weather = weather_object
        self.language = language

    @property
    def image(self) -> Image:
        raise 'It\'s base class. Use this only as an abstraction for creating new classes.'
