import google.generativeai as genai
import json

CONFIG_FILE = 'config.json'
def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)
CONFIG = load_config()

MAX_HISTORY = CONFIG.get("MAX_HISTORY")
HISTORY_FILE = CONFIG.get("HISTORY_FILE")
GEMINI_API = CONFIG.get("GEMINI_API")

genai.configure(api_key=GEMINI_API)

text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}
image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 512,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

text_model = genai.GenerativeModel(model_name="gemini-1.0-pro-latest", generation_config=text_generation_config, safety_settings=safety_settings)
image_model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest", generation_config=image_generation_config, safety_settings=safety_settings)

def send_ai(text):
    response = text_model.generate_content(text)
    if response._error:
        return "❌" + str(response._error)
    return response.text

def load_message_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_message_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def update_message_history(username, user_message, ai_response, ai_status):
    message_history = load_message_history()
    if username not in message_history:
        message_history[username] = []

    message_history[username].append({
        "message": user_message,
        "text": ai_response,
        "status": ai_status
    })
    if len(message_history[username]) > MAX_HISTORY:
        message_history[username].pop(0)

    save_message_history(message_history)
