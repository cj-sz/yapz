# yapz

```bash
pip3 install keyboard hugchat python-dotenv
```

Make a file called `.env` in this directory and add your HuggingFace login credentials:

```.env
EMAIL="email@example.com"
PASSWORD="password"
```

`yap.md` keywords

ALT-Y to send your prompt. Make sure the markdown file is saved beforehand.

end: terminate the conversation and program.
switch: terminate the conversation and change models. TODO
new: terminate the conversation and start a new one with the same model.

Whenever a conversation is terminated it is logged.

I am going to be adjusting this a lot