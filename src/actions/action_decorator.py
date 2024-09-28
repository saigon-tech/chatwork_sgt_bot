import os
import importlib
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.utils.openai_helper import OpenAIHelper
from src.utils.web_utils import WebHelper


class Action(ABC):
    def __init__(self):
        self.openai_helper = OpenAIHelper()

    @abstractmethod
    def execute(
        self, room_id: str, account_id: str, message: str, web_helper: WebHelper
    ) -> Any:
        pass


class ActionRegistry:
    _actions: Dict[str, Dict[str, Any]] = {}
    _web_helper = WebHelper()

    @classmethod
    def register(cls, intent: str, description: str):
        def decorator(action_class: type):
            if not issubclass(action_class, Action):
                raise TypeError(f"{action_class.__name__} must inherit from Action")
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
    def execute_action(
        cls, intent: str, room_id: str, account_id: str, message: str
    ) -> Any:
        action = cls.get_action(intent)
        return (
            action.execute(room_id, account_id, message, cls._web_helper)
            if action
            else None
        )

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
