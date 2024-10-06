import requests
from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper
from src.utils.logger import logger

action = "weather"
description = "Forecast weather report for a given location or city or forecast weather request"


@ActionRegistry.register(action, description)
class WeatherAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        try:
            # Generate a summary using AI
            location = web_helper.query_ai(
                prompt=(
                    "Only return full city name in text in lower case and space in english:"
                    f"\n\n'{message}'\n\nIf not found city name return 'null'"
                ),
                system_message=(
                    "You are a helpful assistant that return city name in text."
                    "Do not provide additional information or explanation beyond the request."
                ),
                # 'San Fernando del Valle de Catamarca' is a longest city name has 43 character
                max_tokens=43,
            )

            if location == "null":
                location = "ho chi minh"

            # Get message
            weather_message = self._weather_forecast(location)

            return weather_message
        except Exception as e:
            error_message = f"An error occurred while trying to get weather forecast: {str(e)}"
            logger.error(error_message, exc_info=True)
            return "Cannot check the weather forecast for your input."

    def _weather_forecast(self, city):
        # Secret info
        API_URL = self.get_config_value("API_URL")
        API_KEY = self.get_config_value("API_KEY")
        headers = {
            "x-rapidapi-host": "open-weather13.p.rapidapi.com",
            "x-rapidapi-key": API_KEY,
        }
        url = f"{API_URL}/city/{city}/EN"

        # Get weather forecast
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return self._format_response(response.json())
        else:
            raise Exception(f"{response.status_code} {response.text}")

    def _format_response(self, json):
        try:
            name = json["name"]
            country = json["sys"]["country"]
            description = json["weather"][0]["description"]

            temp = self._fahrenheit_to_celsius(json["main"]["temp"])
            temp_min = self._fahrenheit_to_celsius(json["main"]["temp_min"])
            temp_max = self._fahrenheit_to_celsius(json["main"]["temp_max"])

            return (
                f"Current weather of {name} ({country}) is {description}.\n"
                f"Temperature {temp}°C ({temp_min}°C - {temp_max}°C)"
            )
        except Exception as e:
            raise Exception(f"Error formatting weather response: {str(e)}")

    def _fahrenheit_to_celsius(self, fahrenheit):
        return round((fahrenheit - 32) * 5 / 9, 1)
