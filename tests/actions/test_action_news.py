import pytest
from unittest.mock import MagicMock
from src.actions.action_news import NewsAction
from src.utils.web_utils import WebHelper


def test_news_action():
    # Arrange
    mock_web_helper = MagicMock(spec=WebHelper)
    mock_web_helper.fetch_news_headlines.return_value = "1. Test headline 1\n2. Test headline 2\n3. Test headline 3"

    news_action = NewsAction()

    # Act
    result = news_action.execute("room_id", "account_id", "Get me the news", mock_web_helper)

    # Assert
    assert "Here are today's top headlines:" in result
    assert "Test headline 1" in result
    assert "Test headline 2" in result
    assert "Test headline 3" in result


def test_news_action_error():
    # Arrange
    mock_web_helper = MagicMock(spec=WebHelper)
    mock_web_helper.fetch_news_headlines.side_effect = Exception("API Error")

    news_action = NewsAction()

    # Act
    result = news_action.execute("room_id", "account_id", "Get me the news", mock_web_helper)

    # Assert
    assert "An error occurred while fetching news headlines" in result
    assert "API Error" in result
