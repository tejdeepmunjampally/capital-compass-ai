from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_retries=2,
)

def generate_response(prompt):
    response = llm.invoke(prompt)
    return response.content
