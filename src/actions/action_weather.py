from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper
import requests

@ActionRegistry.register("weather", "Weather forecast")
class SummaryAction(Action):
    def execute(
        self, room_id: str, account_id: str, message: str, web_helper: WebHelper
    ) -> str:
        try:
            # Fetch the text content from the URL
            content = web_helper.fetch_url_text(url)

            # Generate a summary using AI
            location = web_helper.query_ai(
                prompt=f"Please return city name in text:\n\n{content}",
                system_message="You are a helpful assistant that return city name in text. Do not provide additional information or explanation beyond the request.",
                max_tokens=100,
            )

            # Get message
            weather_message = self.weather_forecast(location)

            return weather_message
        except Exception as e:
            return f"An error occurred while trying to get weather forecast: {e}"

    def format_response(self, json):
        try:
            name = json["name"]
            country = json["sys"]["country"]
            description = json["weather"][0]["description"] 

            t = json["main"]["temp"]
            temp = round(5 * (t - 32) / 9, 1)
            temMin = json["main"]["temp_min"]
            tempMin =round( 5 * (temMin - 32) / 9, 1)
            temMax = json["main"]["temp_max"]
            tempMax = round(5 * (temMax - 32) / 9, 1)

            return  f"\nThời tiết hiện tại của {name} ({country}) là {description}.\nNhiệt độ {temp}°C ({tempMin}°C - {tempMax}°C)"
        except KeyError as e:
            return f"Lỗi: Thiếu khóa {e}"
        except Exception as e:
            return  f"Đã xảy ra lỗi: {e}"

    def weather_forecast(self, city):
        # Secret info
        api_url = "https://open-weather13.p.rapidapi.com/"
        headers = headers = {
            "x-rapidapi-host": "open-weather13.p.rapidapi.com",
            "x-rapidapi-key": "073922d575msh362e38820e8e6e2p129d8fjsn3537b7039650", 
        }
        url = api_url + "/city/" + city + "/VI"

        # Get weather forecast
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return self.format_response(response.json())
        else:
            return f"Lỗi: {response.status_code}, {response.text}"
