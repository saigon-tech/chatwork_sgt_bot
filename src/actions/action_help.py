from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper


@ActionRegistry.register('help', 'Get help on available commands')
class HelpAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        actions = ActionRegistry.get_all_actions()
        help_text = "Available commands:\n\n"
        for intent, action_info in actions.items():
            help_text += f"/{intent}: {action_info['description']}\n"
        return help_text
