import os
import sqlite3

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from utils.database import insert_data
from utils.generation import generate_description_and_examples

# Load environment variables from .env file
load_dotenv()

# Read the OPENAI_API_KEY from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Streamlit app
st.title("Wortschatz 📖")

# Generate button
name = st.text_input("Neu Wort")

if st.button("Einfügen"):
    if name:
        generated_text = generate_description_and_examples(name)
        try:
            wort = generated_text.split("Wort:")[1].split("Beschreibung:")[0]
            beschreibung = generated_text.split("Beschreibung:")[1].split("Beispiel:")[
                0
            ]
            beispiele = generated_text.split("Beispiel:")[1].split("Ins Englische:")[0]
            englische = generated_text.split("Ins Englische:")[1]
            insert_data(wort, beschreibung, beispiele, englische)
            st.success("Daten erfolgreich eingefügt!")
        except IndexError:
            st.warning("Daten nicht erfolgreich eingefügt.")
    else:
        st.warning("Ungültig")

st.subheader("Aktueller Wortschatz")
conn = sqlite3.connect("vocabulary.db")
cursor = conn.cursor()
df = pd.read_sql("SELECT * FROM names_definitions", conn)
conn.close()


df.index = df["Wort"]
st.table(df["Beschreibung"])
st.info("No data available in the database.")
