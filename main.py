import os
import re
import json

from src import ai 
from src import nerv

CONFIG_FILE = 'config.json'
def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)
CONFIG = load_config()

MAX_HISTORY = CONFIG.get("MAX_HISTORY")
USERNAME = CONFIG.get("USERNAME")

with open('prompt.txt', 'r') as dosya:
    prompt = dosya.read()

def main():
    os.system("clear")
    while True:
        try:
            user_input = input(f"<{USERNAME}> ").strip()

            if user_input.startswith("poweroff"):
                break

            if user_input.startswith("clear"):
                os.system("clear")
                continue

            response_json = ai.send_ai(f"{prompt}\n ### {user_input} ###")
            response = json.loads(response_json)
            ai_status = response["status"]
            ai_response = response["text"]

            ai.update_message_history(USERNAME, user_input, ai_response, ai_status)
            nerv.print_colored(f"<Makise> {ai_response}", ai_status)

            #response = ai.send_ai(f"{prompt}\n### {user_input} ###")
            #print(f"<monika> {response}")

        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    main()
