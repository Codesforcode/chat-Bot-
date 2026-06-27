from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# model = init_chat_model(
#     "mistral-small-latest",
#     model_provider="mistralai"
# )
model = ChatMistralAI(
    model="mistral-small-latest"
)


messages = []


user = input("You: ")

messages.append(HumanMessage(content=user))
response = model.invoke(messages)
messages.append(AIMessage(content=response.content))

print("AI:", response.content)