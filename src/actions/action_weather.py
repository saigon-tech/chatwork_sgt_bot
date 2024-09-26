from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper


@ActionRegistry.register('weather', 'Get the current weather for a location')
class WeatherAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        # This is a placeholder. In a real implementation, you would:
        # 1. Extract the location from the message
        # 2. Call a weather API to get the weather data
        # 3. Format and return the weather information
        return "The weather in Tokyo is sunny with a high of 25°C (77°F)."
