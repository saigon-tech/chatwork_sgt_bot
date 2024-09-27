import requests
from bs4 import BeautifulSoup
from src.utils.openai_helper import OpenAIHelper
from src.utils.logger import logger


class WebHelper:
    def __init__(self):
        self.openai_helper = OpenAIHelper()

    def fetch_url_html(self, url: str) -> str:
        """
        Fetch the full HTML content from a given URL.
        
        :param url: The URL to fetch content from
        :return: Raw HTML content of the webpage
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching URL: {e}")
            raise Exception(f"Error fetching URL: {e}")

    def fetch_url_text(self, url: str, max_chars: int = None) -> str:
        """
        Fetch and extract text content from a given URL.
        
        :param url: The URL to fetch content from
        :param max_chars: Maximum number of characters to extract (optional)
        :return: Extracted text content
        """
        try:
            html_content = self.fetch_url_html(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            text = ' '.join([p.text for p in soup.find_all('p')])
            return text[:max_chars] if max_chars else text
        except Exception as e:
            logger.error(f"Error processing webpage content: {e}")
            raise Exception(f"Error processing webpage content: {e}")

    def query_ai(self, prompt: str, system_message: str = "You are a helpful assistant.", max_tokens: int = 500) -> str:
        """
        Query AI model to generate text based on a prompt.
        
        :param prompt: The prompt to generate text from
        :param system_message: The system message to set the context
        :param max_tokens: Maximum number of tokens to generate
        :return: Generated text
        """
        return self.openai_helper.generate_text(prompt, system_message, max_tokens)
