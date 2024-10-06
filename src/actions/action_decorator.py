import os
import importlib
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.utils.openai_helper import OpenAIHelper
from src.utils.web_utils import WebHelper
from src.utils.logger import logger
from src.extensions import cache
from src.model.config import Config


class Action(ABC):
    def __init__(self):
        self.openai_helper = OpenAIHelper()
        if not hasattr(self.__class__, "action"):
            self.__class__.action = self.__class__.__name__.lower().replace("action", "")

    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_config_value(self, key):
        full_key = f"{self.__class__.action.upper()}.{key}"
        return Config.get_value_by_key(full_key)

    @abstractmethod
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> Any:
        pass

    @classmethod
    def test_execute(
        cls, message: str, room_id: str = "test_room", account_id: str = "test_account"
    ):
        """
        A helper method to test the execute method of an Action.

        :param message: The message to process
        :param room_id: A mock room ID (default: "test_room")
        :param account_id: A mock account ID (default: "test_account")
        :return: The result of the execute method
        """
        from src.main import create_app

        app = create_app()
        with app.app_context():
            web_helper = WebHelper()
            action_instance = cls()
            return action_instance.execute(room_id, account_id, message, web_helper)


class ActionRegistry:
    _actions: Dict[str, Dict[str, Any]] = {}
    _web_helper = WebHelper()

    @classmethod
    def register(cls, intent: str, description: str):
        def decorator(action_class: type):
            if not issubclass(action_class, Action):
                raise TypeError(f"{action_class.__name__} must inherit from Action")

            action_class.action = intent

            cls._actions[intent] = {
                "handler": action_class(),
                "description": description,
            }
            return action_class

        return decorator

    @classmethod
    def get_action(cls, intent: str) -> Optional[Action]:
        return cls._actions.get(intent, {}).get("handler")

    @classmethod
    def execute_action(cls, intent: str, room_id: str, account_id: str, message: str) -> Any:
        action = cls.get_action(intent)
        if action:
            try:
                return action.execute(room_id, account_id, message, cls._web_helper)
            except Exception as e:
                logger.error(f"Unhandled error in action '{intent}': {str(e)}", exc_info=True)
                return "An unexpected error occurred while processing your request."
        else:
            return None

    @classmethod
    def get_all_intents(cls) -> List[str]:
        return list(cls._actions.keys())

    @classmethod
    def get_all_actions(cls) -> Dict[str, Dict[str, Any]]:
        return cls._actions


def load_actions() -> None:
    actions_dir = os.path.dirname(__file__)
    for filename in os.listdir(actions_dir):
        if (
            filename.startswith("action_")
            and filename.endswith(".py")
            and filename != "action_decorator.py"
        ):
            module_name = f"src.actions.{filename[:-3]}"
            importlib.import_module(module_name)


# Load actions when the module is imported
load_actions()
