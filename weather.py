import pyowm
from pyowm.utils.config import get_default_config


class Weather:
    detailed_status: str
    wind: dict
    humidity: int
    temperature: dict
    rain: dict
    clouds: int

    def __init__(self, location: str, language: str = 'ru', temperature_type: str = 'celsius'):
        self.location = location
        self.temperature_type = temperature_type

        self.config_dict = get_default_config()
        self.config_dict['language'] = language

        owm = pyowm.OWM('61d202e168925f843260a7f646f65118', self.config_dict)
        self.mgr = owm.weather_manager()

    def get_current(self):
        observation = self.mgr.weather_at_place(self.location)
        w = observation.weather

        self.detailed_status = w.detailed_status
        self.wind = w.wind()
        self.humidity = w.humidity
        self.temperature = w.temperature(self.temperature_type)
        self.rain = w.rain
        self.clouds = w.clouds
