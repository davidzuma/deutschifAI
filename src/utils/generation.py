import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Function to generate description and examples using GPT-3.5
@st.cache_data
def generate_description_and_examples(name):
    prompt = f"""Generate a detailed and concise description (2 lines) and one example in German for the word '{name}',
    along with its English translation. For example:

    Wort:Buch
    Beschreibung:Ein Buch ist ein gedrucktes oder digitales Werk, das aus bedruckten Seiten besteht und in der Regel gebunden ist.
    Beispiel:Ich lese gerne Bücher in meiner Freizeit.
    Ins Englische:Book
    """
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)
    response = llm.invoke(prompt)
    st.write(response.content)
    return response.content.strip()
