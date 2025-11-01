from dotenv import load_dotenv
import os
def load_prompt(name):
    with open(f"resources/{name}.txt", "r", encoding="utf8") as file:
        return file.read()

def load_token(name):
    # === Load Telegram bot token ===
    dotenv_path = 'secrets/pondsupportbot2/'+name+'.env'
    load_dotenv(dotenv_path)

    TOKEN = os.getenv(name.upper()+'_TOKEN')
    if not TOKEN:
        raise ValueError(name+' token not found')
    return TOKEN
