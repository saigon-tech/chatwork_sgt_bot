from src.actions.action_decorator import Action, ActionRegistry
from typing import Any


@ActionRegistry.register('news', 'Get the latest news headlines')
class NewsAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: Any) -> str:
        try:
            news = web_helper.fetch_news_headlines()
            return f"Here are today's top headlines:\n\n{news}"
        except Exception as e:
            return f"An error occurred while fetching news headlines: {str(e)}"
