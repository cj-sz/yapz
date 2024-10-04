import os
import time
import keyboard
from datetime import datetime
from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
import threading

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWD = os.getenv('PASSWORD')
METAPROMPT = "use very informal language and slang in your responses. abbreviate words where possible, for instance instead of using because say bc, and instead of as far as i know use afaik. adhere strictly to my requests, and keep your responses concise. be very informal and casual in conversation and discussion. also type your responses in all lowercase. do not use emojis in your responses. make sure to enclose all code snippets with triple backticks like ```, since I'm storing your responses in a markdown file."

# cookies
cookie_path_dir = "./cookies/"
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict(), system_prompt=METAPROMPT)

models = chatbot.get_available_llm_models()

# Select initial model and set up yap.md
print("Available Models:")
for idx, model in enumerate(models):
    print(f"{idx}: {model}")

selected_model_idx = int(input("Enter the number corresponding to the model you'd like to use: "))
chatbot.switch_llm(selected_model_idx)

# Reapply the metaprompt after switching the model
chatbot.new_conversation(system_prompt=METAPROMPT, switch_to=True)

yap_filename = 'yap.md'
date_str = datetime.now().strftime('%Y-%m-%d')

# Make logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# Initialize conversation_num based on existing logs
conversation_num = 1
existing_logs = [f for f in os.listdir('logs') if f.startswith(f'log-{date_str}-')]

if existing_logs:
    # Extract conversation numbers from existing logs
    existing_numbers = [
        int(log.split('-')[-1].split('.')[0]) for log in existing_logs
    ]
    conversation_num = max(existing_numbers) + 1  # Start from the next number

def get_log_filename():
    global conversation_num
    s = f'logs/log-{date_str}-{conversation_num}.md'
    conversation_num += 1
    return s

# Create or overwrite the yap.md file
with open(yap_filename, 'w') as yap_file:
    yap_file.write(f"# Conversation started on {date_str}\n")
    yap_file.write("**You**:\n")

print(f"converse in {yap_filename}. save then alt+y to send prompt. see README for keywords")

def send_prompt():
    # Read the last line from the yap.md file (this should be the user's latest prompt)
    with open(yap_filename, 'r') as yap_file:
        lines = yap_file.readlines()

    # Get the latest user prompt from the last non-empty line
    user_prompt = lines[-1].strip()

    # Save log and handle prompts "exit", "new", and "switch"
    if user_prompt == "exit":
        # Save the conversation log when exiting
        log_filename = get_log_filename()
        os.rename(yap_filename, log_filename)
        print(f"Conversation saved to {log_filename}\n")
        # This is probably bad practice but who cares
        os._exit(0)  # Forcefully exit the program
    
    # # TODO filling this in later cause it doesn't work (just a placeholder)
    # # for now you gotta just restart the program
    # elif user_prompt == "switch":
    #     # Save the conversation log
    #     log_filename = get_log_filename()
    #     os.rename(yap_filename, log_filename)
        
    #     # Ask for model selection in the markdown file
    #     with open(yap_filename, 'w') as yap_file:
    #         yap_file.write(f"# Conversation ended. Please select a new model:\n")
    #         for idx, model in enumerate(models):
    #             yap_file.write(f"{idx}: {model}\n")
    #         yap_file.write("**You**:\n")
        
    #     print(f"Conversation saved to {log_filename}. Please select a new model in {yap_filename}.")
    #     return True  # Continue the loop

    elif user_prompt == "new":
        # Save the conversation log and restart with the same model
        log_filename = get_log_filename()
        os.rename(yap_filename, log_filename)
        
        # Clear the yap.md for the new conversation
        with open(yap_filename, 'w') as yap_file:
            yap_file.write(f"# Conversation restarted on {date_str}\n")
            yap_file.write("**You**:\n")

        print(f"Conversation saved to {log_filename}. Starting a new conversation with the same model.")
        return True  # Continue the loop

    # Send the user's prompt and wait for the model's response
    message_result = chatbot.chat(user_prompt)
    response_str = message_result.wait_until_done()

    # Print and log the model's response to yap.md
    with open(yap_filename, 'a') as yap_file:
        yap_file.write(f"\n**Model**:\n{response_str}\n**You**:\n")

    print(f"Response from the model printed in {yap_filename}.")
    return True  # Continue the loop

def listen_for_keypress():
    keyboard.add_hotkey('alt+y', send_prompt)

# Start a thread to listen for key presses
keypress_thread = threading.Thread(target=listen_for_keypress, daemon=True)
keypress_thread.start()

# Keep the main thread alive to allow the keypress listener to work
while True:
    time.sleep(1)  # Sleep to reduce CPU usage
