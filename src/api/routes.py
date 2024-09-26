from flask import Blueprint, request, jsonify
from src.bot.chatwork_bot import ChatworkBot
from src.utils.signature_verifier import verify_signature
from src.utils.logger import logger
from celery import shared_task

api_bp = Blueprint('api', __name__)
bot = ChatworkBot()


@shared_task
def process_chatwork_message(message, room_id, account_id):
    result = bot.handle_message(message, room_id, account_id)
    if result['status'] != 'success':
        logger.error(f"Error processing message: {result['message']}")


@api_bp.route('/callback', methods=['POST'])
def chatwork_callback():
    signature = request.args.get('chatwork_webhook_signature')
    if not signature:
        logger.error("Missing signature")
        return jsonify({"status": "error", "message": "Missing signature"}), 400

    payload = request.get_data()
    if not verify_signature(payload, signature):
        logger.error("Signature verification failed")
        return jsonify({"status": "error", "message": "Invalid signature"}), 401

    data = request.json
    room_id = data.get('webhook_event', {}).get('room_id')
    message = data.get('webhook_event', {}).get('body')
    account_id = data.get('webhook_event', {}).get('from_account_id')

    if not all([room_id, message, account_id]):
        logger.error("Missing required data in webhook payload")
        return jsonify({"status": "error", "message": "Missing required data"}), 400

    # Process the message asynchronously
    process_chatwork_message.delay(message, room_id, account_id)

    return jsonify({"status": "success", "message": "Webhook received and processing"}), 200


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200
