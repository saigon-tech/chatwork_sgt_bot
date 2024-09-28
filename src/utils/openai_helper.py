from openai import OpenAI
from src.config import Config
from src.utils.logger import logger


class OpenAIHelper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIHelper, cls).__new__(cls)
            cls._instance.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        return cls._instance

    def generate_text(
        self,
        prompt,
        system_message="You are a helpful assistant.",
        max_tokens=150,
    ):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {e}")
            return None
