from src.actions.action_decorator import ActionRegistry
from src.utils.interpreter import interpret_message
from src.utils.chatwork_api import send_message_to_room
from src.utils.logger import logger
from typing import Optional


class ChatworkBot:
    def handle_message(self, message: str, room_id: str, account_id: str, message_id: str) -> dict:
        try:
            cleaned_message = self._clean_message(message)
            if cleaned_message is None:
                return {
                    "status": "skipped",
                    "message": "Message starts with [toall], skipping processing",
                }

            intent = self._get_intent(cleaned_message)
            response = self._generate_response(intent, room_id, account_id, cleaned_message)
            self._send_response(room_id, account_id, message_id, response)
            return {
                "status": "success",
                "message": "Response sent as reply to user in Chatwork room",
            }
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _clean_message(self, message: str) -> Optional[str]:
        cleaned_message = message.strip()
        if "[toall]" in cleaned_message.lower():
            return None
        if cleaned_message.startswith("[To:"):
            cleaned_message = cleaned_message.split("]", 1)[-1].strip()
        return cleaned_message

    def _get_intent(self, message: str) -> str:
        return interpret_message(message)

    def _generate_response(self, intent: str, room_id: str, account_id: str, message: str) -> str:
        response = ActionRegistry.execute_action(intent, room_id, account_id, message)
        if response is None:
            response = self._get_default_response(intent)
        return response

    def _get_default_response(self, intent: str) -> str:
        if intent == "greeting":
            return "Hello! How can I assist you today?"
        return "I don't understand that command. Can you please rephrase or ask for help?"

    def _send_response(
        self, room_id: str, account_id: str, message_id: str, response: str
    ) -> None:
        reply = f"[rp aid={account_id} to={room_id}-{message_id}]\n{response}"
        send_message_to_room.delay(room_id, reply)
