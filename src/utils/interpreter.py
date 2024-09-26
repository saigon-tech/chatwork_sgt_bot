from openai import OpenAI
from src.config import Config
from src.actions.action_decorator import ActionRegistry

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)


def interpret_message(message):
    try:
        valid_intents = ActionRegistry.get_all_intents() + ['greeting', 'unknown']
        intent_descriptions = {intent: ActionRegistry._actions.get(intent, {}).get('description', '') for intent in
                               valid_intents}
        intent_descriptions['greeting'] = "Respond to a greeting"
        intent_descriptions['unknown'] = "Intent not recognized"

        intents_str = ', '.join(f"'{intent}': {description}" for intent, description in intent_descriptions.items())

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"You are an AI assistant that interprets user messages and extracts the intent. The possible intents and their descriptions are: {intents_str}. Respond with only the intent."},
                {"role": "user", "content": f"Extract the intent from this message: '{message}'"}
            ],
            max_tokens=50
        )

        intent = response.choices[0].message.content.strip().lower()

        if intent not in valid_intents:
            intent = 'unknown'

        return intent
    except Exception as e:
        print(f"Error in interpreting message: {e}")
        return 'unknown'
