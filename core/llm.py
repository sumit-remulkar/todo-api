from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3"
)

def get_llm():
    return llm