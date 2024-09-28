import hmac
import hashlib
import base64
import urllib.parse
from src.config import Config


def verify_signature(payload, signature):
    """Verify the webhook signature."""
    webhook_token = Config.CHATWORK_WEBHOOK_TOKEN
    webhook_token += "=" * ((4 - len(webhook_token) % 4) % 4)
    webhook_token_bytes = base64.b64decode(webhook_token)

    computed_signature = base64.b64encode(
        hmac.new(webhook_token_bytes, payload, hashlib.sha256).digest()
    ).decode("utf-8")

    decoded_signature = urllib.parse.unquote(signature)
    return hmac.compare_digest(decoded_signature, computed_signature)
