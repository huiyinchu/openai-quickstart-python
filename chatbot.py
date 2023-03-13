import os
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, download_loader

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

SimpleWebPageReader = download_loader("SimpleWebPageReader")
loader = SimpleWebPageReader()
documents = loader.load_data(
    urls=['https://bootcamp.uxdesign.cc/a-step-by-step-guide-to-building-a-chatbot-based-on-your-own-documents-with-gpt-2d550534eea5'])

# Construct a simple vector index
index = GPTSimpleVectorIndex(documents)
# Querying the index
response = index.query('What is this website talking about?')
print(response)
