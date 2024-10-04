import os
import time
from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch email and password from environment variables
EMAIL = os.getenv('EMAIL')
PASSWD = os.getenv('PASSWORD')

# Set cookie path directory
cookie_path_dir = "./cookies/"  # NOTE: trailing slash (/) is required to avoid errors
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Define metaprompt to be used globally
METAPROMPT = "use very informal language and slang in your responses. abbreviate words where possible, for instance instead of using because say bc, and instead of as far as i know use afaik. adhere strictly to my requests, and keep your responses concise. be very informal and casual in conversation and discussion. also type your responses in all lowercase. do not use emojis in your responses."

# Create a ChatBot object with the metaprompt
chatbot = hugchat.ChatBot(cookies=cookies.get_dict(), system_prompt=METAPROMPT)

# Get the available models and prompt user for model selection
models = chatbot.get_available_llm_models()
print("Available Models:")
for idx, model in enumerate(models):
    print(f"{idx}: {model}")

# Prompt user to select a model by index
selected_model_idx = int(input("Enter the number corresponding to the model you'd like to use: "))
chatbot.switch_llm(selected_model_idx)

# Reapply the metaprompt after switching the model
chatbot.new_conversation(system_prompt=METAPROMPT, switch_to=True)

print("\nType 3 to end conversating.\n")

# Loop to keep the conversation going until the user types 'exit'
while True:
    # Prompt user to input their message or control command
    user_prompt = input("You: ")

    # Check for control commands
    if user_prompt == "1":
        chatbot.new_conversation(system_prompt=METAPROMPT, switch_to=True)
        print("\nStarted a new chat with the same model!\n")
        continue  # Continue to the next iteration

    if user_prompt == "2":
        # Prompt user for model selection
        print("Available Models:")
        for idx, model in enumerate(models):
            print(f"{idx}: {model}")
        selected_model_idx = int(input("Enter the number corresponding to the model you'd like to use: "))
        chatbot.switch_llm(selected_model_idx)
        chatbot.new_conversation(system_prompt=METAPROMPT, switch_to=True)
        print("\nBegin new chat:\n")
        continue  # Continue to the next iteration

    if user_prompt == "3":
        break  # Exit the loop

    # Send the user's prompt and wait for the model's response
    message_result = chatbot.chat(user_prompt)
    response_str = message_result.wait_until_done()

    # Print the model's response one character at a time
    print("Model: ", end="", flush=True)  # Print 'Model: ' without newline
    for char in response_str:
        print(char, end="", flush=True)  # Print each character
        time.sleep(0.001)  # Wait for 0.001 seconds between characters
    print("\n")  # Newline after the response
