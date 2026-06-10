from langchain_ollama import ChatOllama

llm = ChatOllama(model="phi3:mini")

def generate_response(prompt):
    response = llm.invoke(prompt)
    return response.content