from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

load_dotenv()

messages = [{"role": "system", "content": "You are a helpful assistant."}, ]
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI()
chat_model = ChatOpenAI()

# test predict
text = 'hi!'
llm.predict(text)
chat_model.predict(text)

# test promptTemplate
prompt = PromptTemplate.from_template(
    'What is a goog name for a company that makes {product}?')
prompt.format(product='colorful socks')


template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

chat_prompt.format_messages(
    input_language="English", output_language="French", text="I love programming.")


# test parser
class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        return text.strip.split(',')


CommaSeparatedListOutputParser.parse('hi, world')

'''
We can now combine all these into one chain. This chain will take input variables, pass those to a 
prompt template to create a prompt, pass the prompt to a language model, and then pass the output through
 an (optional) output parser. This is a convenient way to bundle up a modular piece of logic. Let's see it in action!
'''


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more."""
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])
chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()
chain.invoke({"text": "colors"})
# >> ['red', 'blue', 'green', 'yellow', 'orange']
