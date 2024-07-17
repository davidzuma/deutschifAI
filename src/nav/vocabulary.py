import os

import streamlit as st
from dotenv import load_dotenv

from utils.database import get_names_and_definitions_df, insert_data
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
names_and_definitions_df = get_names_and_definitions_df()

if not names_and_definitions_df.empty:
    names_and_definitions_df.index = names_and_definitions_df["Wort"]
    st.table(names_and_definitions_df["Beschreibung"])
else:
    st.info("No data available in the database.")
