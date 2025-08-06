from langchain.llms import MistralAI
import os

def summarize_answer(text):
    llm = MistralAI(api_key=os.getenv("MISTRAL_API_KEY"))
    return llm.predict(f"Summarize this: {text}")
