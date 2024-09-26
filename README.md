# SGT Chatwork Bot

A modular, extensible chatbot for SGT Team. The bot listens for mentions in Chatwork rooms, interprets user messages, and performs predefined actions like fetching the latest news or summarizing website content. The bot is designed to be easily extendable, allowing the addition of new commands and functionalities with minimal effort.

## Features

- **Mention-based interaction:** The bot responds only when mentioned in the message, ensuring it doesn't interfere with other discussions.
- **Predefined actions:** The bot currently supports the following actions:
  - `/news`: Fetches the latest news headlines.
  - `/summary <url>`: Takes a URL as input, crawls the page content, and provides a short summary.
  - `/weather`: Provides current weather information (placeholder implementation).
  - `/help`: Lists all available commands and their descriptions.
- **Modular architecture:** Easily extend the bot by adding new action scripts.
- **Command interpretation:** The bot uses GPT-3.5 to understand user input and map it to predefined commands.
- **Asynchronous processing:** Uses Celery for background task processing.

## Requirements

- Python 3.9+
- Flask
- Celery
- Redis (for Celery broker)
- OpenAI API key
- Chatwork API token

## Project Structure
chatwork-bot/
│
├── app.py                   # Main Flask application
├── config.py                # Configuration file (e.g., API keys, URLs)
├── requirements.txt         # Python dependencies (Flask, Requests, etc.)
├── actions/                 # Directory for all bot actions (modular commands)
│   ├── __init__.py          # Init file for the actions module
│   ├── news.py              # News action logic
│   ├── summary.py           # Summary action logic
│   └── action_registry.py   # Registry to manage and route actions
│
├── utils/                   # Utility functions, helpers (e.g., web scraping, API calls)
│   ├── __init__.py          # Init file for utils module
│   ├── crawler.py           # Utility for crawling URLs
│   └── formatter.py         # Utility for formatting responses (Optional)
|   └── interpret.py         # GPT-3.5 powered user input interpretation
|
├── logs/                    # Directory for logging (Optional)
│   └── bot.log              # Log file for bot activities (Optional)
│
├── templates/               # HTML templates (if needed for message formatting)
│
└── tests/                   # Unit tests for bot functionality
    ├── test_news.py         # Test for news action
    ├── test_summary.py      # Test for summary action
    └── __init__.py          # Init file for tests module

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## How to Add a New Action

To add a new action to the bot, follow these steps:

1. Create a new file in the `src/actions/` directory, named `action_<your_action_name>.py`.
2. In this file, define a new class that inherits from `Action` and implements the `execute` method. For example:

```
from src.actions.action_decorator import Action, ActionRegistry
from typing import Any

@ActionRegistry.register('your_action_name', 'Description of your action')
class YourActionClass(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: Any) -> str:
        # Implement your action logic here
        return "Your action response"
```

3. The `@ActionRegistry.register` decorator automatically registers your action with the bot. The first parameter is the command name, and the second is a brief description.

4. Implement your action logic in the `execute` method. This method receives:
   - `room_id`: The Chatwork room ID where the message was received.
   - `account_id`: The Chatwork account ID of the user who sent the message.
   - `message`: The full message text.
   - `web_helper`: An instance of `WebHelper` for making web requests or using OpenAI.

5. Return a string from the `execute` method. This string will be sent as a response to the Chatwork room.

6. Your new action will be automatically loaded and available to use in Chatwork by mentioning the bot and using the command name you specified in the `@ActionRegistry.register` decorator.
