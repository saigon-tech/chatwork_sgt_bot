from unittest.mock import MagicMock, patch
from src.actions.action_decorator import ActionRegistry, Action
from src.utils.web_utils import WebHelper


class BaseTestAction(Action):
    def __init__(self):
        super().__init__()

    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        return "Test action executed"


def test_action_registration():
    # Arrange
    ActionRegistry._actions.clear()  # Clear existing actions for this test

    # Act
    @ActionRegistry.register("test", "Test action description")
    class TestActionClass(BaseTestAction):
        pass

    # Assert
    assert "test" in ActionRegistry._actions
    assert isinstance(ActionRegistry._actions["test"]["handler"], TestActionClass)
    assert ActionRegistry._actions["test"]["description"] == "Test action description"


def test_get_action():
    # Arrange
    ActionRegistry._actions.clear()  # Clear existing actions for this test

    @ActionRegistry.register("test", "Test action description")
    class TestActionClass(BaseTestAction):
        pass

    # Act
    action = ActionRegistry.get_action("test")

    # Assert
    assert isinstance(action, TestActionClass)


def test_execute_action():
    # Arrange
    ActionRegistry._actions.clear()  # Clear existing actions for this test

    @ActionRegistry.register("test", "Test action description")
    class TestActionClass(BaseTestAction):
        pass

    # Mock the WebHelper
    mock_web_helper = MagicMock(spec=WebHelper)

    # Patch the _web_helper in ActionRegistry
    with patch.object(ActionRegistry, "_web_helper", mock_web_helper):
        # Act
        result = ActionRegistry.execute_action("test", "room_id", "account_id", "Test message")

        # Assert
        assert result == "Test action executed"


def test_get_all_intents():
    # Arrange
    ActionRegistry._actions.clear()  # Clear existing actions for this test

    @ActionRegistry.register("test1", "Test action 1")
    class TestAction1(BaseTestAction):
        pass

    @ActionRegistry.register("test2", "Test action 2")
    class TestAction2(BaseTestAction):
        pass

    # Act
    intents = ActionRegistry.get_all_intents()

    # Assert
    assert set(intents) == {"test1", "test2"}


def test_get_all_actions():
    # Arrange
    ActionRegistry._actions.clear()  # Clear existing actions for this test

    @ActionRegistry.register("test1", "Test action 1")
    class TestAction1(BaseTestAction):
        pass

    @ActionRegistry.register("test2", "Test action 2")
    class TestAction2(BaseTestAction):
        pass

    # Act
    actions = ActionRegistry.get_all_actions()

    # Assert
    assert set(actions.keys()) == {"test1", "test2"}
    assert actions["test1"]["description"] == "Test action 1"
    assert actions["test2"]["description"] == "Test action 2"
