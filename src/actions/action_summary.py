from src.actions.action_decorator import Action, ActionRegistry
from typing import Any


@ActionRegistry.register('summary', 'Summarize the content of a given URL')
class SummaryAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: Any) -> str:
        # Extract URL from the message
        words = message.split()
        url = next((word for word in words if word.startswith('http')), None)

        if not url:
            return "Please provide a valid URL to summarize."

        try:
            text = web_helper.extract_text_from_url(url)
            summary = web_helper.summarize_text(text)
            return f"Summary of {url}:\n\n{summary}"
        except Exception as e:
            return f"An error occurred while trying to summarize the URL: {str(e)}"
