import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@st.cache_data
def generate_description_and_examples(name):
    prompt = f"""You are an German teacher.
    Generate a detailed and concise description (2 lines) using A2 German level and one example in German for the word '{name}',
    along with its English translation. If there are spelling errors, correct it when using the word.


    **Example output:**
    Wort:Buch
    Beschreibung:Ein Buch ist ein gedrucktes oder digitales Werk, das aus bedruckten Seiten besteht und in der Regel gebunden ist.
    Beispiel:Ich lese gerne Bücher in meiner Freizeit.
    Ins Englische:Book
    **End of Example**

    Provide always the structure above and nothing else.
    """
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
    response = llm.invoke(prompt)
    return response.content.strip()
