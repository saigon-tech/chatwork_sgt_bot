from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper


@ActionRegistry.register("summary", "Summarize the content of a given URL")
class SummaryAction(Action):
    def execute(
        self, room_id: str, account_id: str, message: str, web_helper: WebHelper
    ) -> str:
        # Extract URL from the message
        words = message.split()
        url = next((word for word in words if word.startswith("http")), None)

        if not url:
            return "Please provide a valid URL to summarize."

        try:
            # Fetch the text content from the URL
            content = web_helper.fetch_url_text(url)

            # Generate a summary using AI
            summary = web_helper.query_ai(
                prompt=f"Please summarize the following text in about 3-4 sentences:\n\n{content}",
                system_message="You are a helpful assistant that summarizes text.",
                max_tokens=300,
            )

            return f"Summary of {url}\n\n{summary}"
        except Exception as e:
            return f"An error occurred while trying to summarize the URL: {str(e)}"
