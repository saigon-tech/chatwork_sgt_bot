import pytest
from unittest.mock import patch, MagicMock
import requests
from src.utils.web_utils import WebHelper


@pytest.fixture
def web_helper():
    return WebHelper()


def test_extract_text_from_url():
    web_helper = WebHelper()
    url = "https://example.com"
    max_chars = 1000

    # Mock the requests.get function
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = "<html><body><p>Test paragraph 1</p><p>Test paragraph 2</p></body></html>"
        mock_get.return_value = mock_response

        result = web_helper.extract_text_from_url(url, max_chars)

        assert result == "Test paragraph 1 Test paragraph 2"
        mock_get.assert_called_once_with(url)


def test_extract_text_from_url_max_chars(web_helper):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = '<html><body><p>Test content</p><p>More content</p></body></html>'
        mock_get.return_value = mock_response

        result = web_helper.extract_text_from_url('https://example.com', max_chars=10)
        assert result == 'Test conte'


def test_extract_text_from_url_error(web_helper):
    with patch('requests.get', side_effect=requests.RequestException("Connection error")):
        with pytest.raises(Exception) as exc_info:
            web_helper.extract_text_from_url('https://example.com')
        assert "Error fetching URL" in str(exc_info.value)


def test_web_helper_extract_text_from_url(web_helper):
    with patch.object(web_helper, 'extract_text_from_url') as mock_extract:
        mock_extract.return_value = "Extracted text"
        result = web_helper.extract_text_from_url('https://example.com')
        assert result == "Extracted text"
        mock_extract.assert_called_once_with('https://example.com')


def test_web_helper_summarize_text(web_helper):
    with patch.object(web_helper.openai_helper, 'generate_text') as mock_generate:
        mock_generate.return_value = "Summarized text"
        result = web_helper.summarize_text("Long text to summarize")
        assert result == "Summarized text"
        mock_generate.assert_called_once_with(
            "Please summarize the following text in about 3-4 sentences:\n\nLong text to summarize",
            "You are a helpful assistant that summarizes text.",
            300
        )


def test_web_helper_fetch_news_headlines(web_helper):
    with patch.object(web_helper.openai_helper, 'generate_text') as mock_generate:
        mock_generate.return_value = "1. Headline 1\n2. Headline 2\n3. Headline 3"
        result = web_helper.fetch_news_headlines()
        assert result == "1. Headline 1\n2. Headline 2\n3. Headline 3"
        mock_generate.assert_called_once_with(
            "Give me the top 3 current news headlines in a concise format.",
            "You are a helpful news assistant."
        )
