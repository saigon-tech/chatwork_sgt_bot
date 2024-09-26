import requests
from bs4 import BeautifulSoup
from src.utils.openai_helper import OpenAIHelper


class WebHelper:
    def __init__(self):
        self.openai_helper = OpenAIHelper()

    def extract_text_from_url(self, url: str, max_chars: int = 4000) -> str:
        """
        Extract text content from a given URL.
        
        :param url: The URL to extract text from
        :param max_chars: Maximum number of characters to extract (default 4000)
        :return: Extracted text
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from the webpage (this is a basic approach)
            paragraphs = soup.find_all('p')
            text = ' '.join([p.text for p in paragraphs])

            # Limit the text to avoid exceeding token limits
            return text[:max_chars]
        except requests.RequestException as e:
            raise Exception(f"Error fetching URL: {e}")
        except Exception as e:
            raise Exception(f"Error processing webpage content: {e}")

    def summarize_text(self, text: str, max_tokens: int = 300) -> str:
        return self.openai_helper.generate_text(
            f"Please summarize the following text in about 3-4 sentences:\n\n{text}",
            "You are a helpful assistant that summarizes text.",
            max_tokens
        )

    def fetch_news_headlines(self) -> str:
        return self.openai_helper.generate_text(
            "Give me the top 3 current news headlines in a concise format.",
            "You are a helpful news assistant."
        )
