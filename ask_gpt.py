
# https://gist.github.com/Thoxvi/bcd7d7242f59bd1cc1d7b92499ec671b


import openai
import sys
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


class Session:
    def __init__(self, max_length=20):
        self.system_msgs = [
            Message("system", "You are a mischievous artificial assistant."),
        ]
        self.messages = []
        self.max_length = max_length

    def add_message(self, message: Message) -> None:
        if len(self.messages) >= self.max_length:
            self.messages.pop(0)
        self.messages.append(message)

    def make_messages(self) -> list[dict]:
        return [
            msg.to_dict()
            for msg
            in self.system_msgs + self.messages
        ]


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def ask_ai_use_lib(session, new_question):
    msgs = [
        *session.make_messages(),
        {"role": "user", "content": new_question}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            *session.make_messages(),
            {"role": "user", "content": new_question}
        ]
    )
    msg = completion.choices[0].message
    session.add_message(Message("user", new_question))
    session.add_message(Message(msg["role"], msg["content"]))
    return msg["content"]


def main():
    session_map = {}
    ask_ai = ask_ai_use_lib
    user = get_random_string(10)
    print(user)

    if user not in session_map:
        session_map[user] = Session()

    session = session_map[user]
    try:
        while True:
            print("You: ", end="")
            sys.stdout.flush()
            text = sys.stdin.readline()
            if not text:
                break
            print("AI: ", ask_ai(session, text).strip())
            print()
    except KeyboardInterrupt:
        pass
    print("Goodbye!")


if __name__ == "__main__":
    main()
