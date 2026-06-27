from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()
embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)
document = [
    "Hey my name is akash",
    "today i am learning embeddings"
]
vector = embeddings.embed_documents(document)
print((vector))