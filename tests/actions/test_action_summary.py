import pytest
from unittest.mock import MagicMock
from src.actions.action_summary import SummaryAction
from src.utils.web_utils import WebHelper


def test_summary_action():
    # Arrange
    mock_web_helper = MagicMock(spec=WebHelper)
    mock_web_helper.extract_text_from_url.return_value = "This is a test article content."
    mock_web_helper.summarize_text.return_value = "This is a summary of the test article."

    summary_action = SummaryAction()

    # Act
    result = summary_action.execute("room_id", "account_id", "Summarize https://example.com", mock_web_helper)

    # Assert
    assert "Summary of https://example.com:" in result
    assert "This is a summary of the test article." in result


def test_summary_action_no_url():
    # Arrange
    mock_web_helper = MagicMock(spec=WebHelper)
    summary_action = SummaryAction()

    # Act
    result = summary_action.execute("room_id", "account_id", "Summarize this", mock_web_helper)

    # Assert
    assert "Please provide a valid URL to summarize." in result


def test_summary_action_error():
    # Arrange
    mock_web_helper = MagicMock(spec=WebHelper)
    mock_web_helper.extract_text_from_url.side_effect = Exception("Failed to fetch URL")

    summary_action = SummaryAction()

    # Act
    result = summary_action.execute("room_id", "account_id", "Summarize https://example.com", mock_web_helper)

    # Assert
    assert "An error occurred while trying to summarize the URL" in result
    assert "Failed to fetch URL" in result
