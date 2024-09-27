import pytest
from unittest.mock import patch, MagicMock
import requests
from src.utils.web_utils import WebHelper


@pytest.fixture
def web_helper():
    return WebHelper()


def test_fetch_url_text(web_helper):
    url = "https://example.com"
    max_chars = 1000

    with patch.object(web_helper, 'fetch_url_html') as mock_fetch_html:
        mock_fetch_html.return_value = "<html><body><p>Test paragraph 1</p><p>Test paragraph 2</p></body></html>"

        result = web_helper.fetch_url_text(url, max_chars)

        assert result == "Test paragraph 1 Test paragraph 2"
        mock_fetch_html.assert_called_once_with(url)


def test_fetch_url_text_max_chars(web_helper):
    url = "https://example.com"

    with patch.object(web_helper, 'fetch_url_html') as mock_fetch_html:
        mock_fetch_html.return_value = '<html><body><p>Test content</p><p>More content</p></body></html>'

        result = web_helper.fetch_url_text(url, max_chars=10)
        assert result == 'Test conte'


def test_fetch_url_html_error(web_helper):
    with patch('requests.get', side_effect=requests.RequestException("Connection error")):
        with pytest.raises(Exception) as exc_info:
            web_helper.fetch_url_html('https://example.com')
        assert "Error fetching URL" in str(exc_info.value)


def test_fetch_url_text_error(web_helper):
    with patch.object(web_helper, 'fetch_url_html', side_effect=Exception("Processing error")):
        with pytest.raises(Exception) as exc_info:
            web_helper.fetch_url_text('https://example.com')
        assert "Error processing webpage content" in str(exc_info.value)


def test_web_helper_fetch_url_text(web_helper):
    with patch.object(web_helper, 'fetch_url_text') as mock_fetch:
        mock_fetch.return_value = "Extracted text"
        result = web_helper.fetch_url_text('https://example.com')
        assert result == "Extracted text"
        mock_fetch.assert_called_once_with('https://example.com')

# You can keep the existing test_web_helper_extract_text_from_url if you still have that method,
# or remove it if it's no longer part of your WebHelper class.
