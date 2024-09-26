import pytest
from unittest.mock import patch, MagicMock
from src.utils.openai_helper import OpenAIHelper
from src.config import Config


@pytest.fixture
def openai_helper():
    # Reset the singleton instance before each test
    OpenAIHelper._instance = None
    return OpenAIHelper()


def test_singleton_instance():
    helper1 = OpenAIHelper()
    helper2 = OpenAIHelper()
    assert helper1 is helper2


def test_generate_text(openai_helper):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Generated text"

    with patch.object(openai_helper.client.chat.completions, 'create', return_value=mock_response):
        result = openai_helper.generate_text("Test prompt")
        assert result == "Generated text"


def test_generate_text_with_system_message(openai_helper):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Custom generated text"

    with patch.object(openai_helper.client.chat.completions, 'create', return_value=mock_response) as mock_create:
        result = openai_helper.generate_text("Test prompt", "Custom system message")
        assert result == "Custom generated text"

        # Check if the custom system message was used
        calls = mock_create.call_args_list
        assert len(calls) == 1
        assert calls[0][1]['messages'][0]['content'] == "Custom system message"


def test_generate_text_error(openai_helper):
    with patch.object(openai_helper.client.chat.completions, 'create', side_effect=Exception("API error")):
        with patch('builtins.print') as mock_print:
            result = openai_helper.generate_text("Test prompt")
            assert result is None
            mock_print.assert_called_once_with("Error in OpenAI API call: API error")


@patch('src.utils.openai_helper.OpenAI')
def test_openai_client_initialization(mock_openai):
    Config.OPENAI_API_KEY = "test_api_key"
    OpenAIHelper._instance = None  # Reset singleton
    OpenAIHelper()
    mock_openai.assert_called_once_with(api_key="test_api_key")
