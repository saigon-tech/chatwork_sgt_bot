import pytest
from unittest.mock import patch, MagicMock
from src.utils.interpreter import interpret_message
from src.actions.action_decorator import ActionRegistry


# Mock the OpenAI client
@pytest.fixture
def mock_openai():
    with patch('src.utils.interpreter.client') as mock:
        yield mock


# Mock the ActionRegistry
@pytest.fixture
def mock_action_registry():
    with patch('src.utils.interpreter.ActionRegistry') as mock:
        mock.get_all_intents.return_value = ['news', 'summary', 'weather', 'help']
        mock._actions = {
            'news': {'description': 'Get the latest news'},
            'summary': {'description': 'Summarize a URL'},
            'weather': {'description': 'Get weather information'},
            'help': {'description': 'Show available commands'}
        }
        yield mock


def test_interpret_message_news(mock_openai, mock_action_registry):
    mock_openai.chat.completions.create.return_value.choices[0].message.content = 'news'

    result = interpret_message("What's the latest news?")
    assert result == 'news'


def test_interpret_message_summary(mock_openai, mock_action_registry):
    mock_openai.chat.completions.create.return_value.choices[0].message.content = 'summary'

    result = interpret_message("Can you summarize this article for me?")
    assert result == 'summary'


def test_interpret_message_unknown(mock_openai, mock_action_registry):
    mock_openai.chat.completions.create.return_value.choices[0].message.content = 'unknown'

    result = interpret_message("What's the meaning of life?")
    assert result == 'unknown'


def test_interpret_message_greeting(mock_openai, mock_action_registry):
    mock_openai.chat.completions.create.return_value.choices[0].message.content = 'greeting'

    result = interpret_message("Hello there!")
    assert result == 'greeting'


def test_interpret_message_error(mock_openai, mock_action_registry):
    mock_openai.chat.completions.create.side_effect = Exception("API Error")

    result = interpret_message("This should cause an error")
    assert result == 'unknown'


def test_interpret_message_invalid_intent(mock_openai, mock_action_registry):
    mock_openai.chat.completions.create.return_value.choices[0].message.content = 'invalid_intent'

    result = interpret_message("This should return an invalid intent")
    assert result == 'unknown'
