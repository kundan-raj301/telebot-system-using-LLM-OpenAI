from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys

class Reference:
    '''
      A class to store previosly responce from the chatgpt API
    '''
    
    def __init__(self) -> None:
        self.response = ""

load_dotenv()

openai.api_key = os.getenv("OpenAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TOKEN")

# Model Name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token= TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    '''
    This function to clear the previous coversation and context
    '''
    reference.response = ""
    

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives message with '/start' or '/help' command
    """
    
    await message.reply("Hi\nI am TeleBot!\nMy God is Kundan.How can I assist you?")
 
 

@dispatcher.message_handler(commands=['clear'])
async def clear(message:types.Message):
    '''
    A handler to clear the previous conversation and context
    
    '''
    clear_past()
    await message.reply("I've cleared the past conversation and context")


@dispatcher.message_handler(commands=['help'])
async def helper(message:types.Message):
    '''
    A handler to display the help menu.
    
    '''
    help_command = """
    Hi There, I'am ChatGPT Telegram Bot created bu Kundan! Please follow these commands-
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    
    I Hope this helps. :)
    """
   
    await message.reply(help_command)

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

if __name__ == "__main__":
    executor.start_polling(dispatcher,skip_updates=True)