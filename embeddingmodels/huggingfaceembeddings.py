from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-miniLM-L6-v2"
)
texts = [
    "hello to  all"
]
vector = embedding.aembed_documents(texts)
print(vector)



