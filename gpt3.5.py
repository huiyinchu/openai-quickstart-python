# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import os
from dotenv import load_dotenv

load_dotenv()

messages = [{"role": "system", "content": "You are a helpful assistant."}, ]
openai.api_key = os.getenv("OPENAI_API_KEY")

while True:
    message = input("Yinchu: ")
    if message:
        messages.append({"role": "user", "content": message},)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response.choices[0].message.content
    print(f"ChatGPT: {reply}\n")
    messages.append({"role": "assistant", "content": reply})
