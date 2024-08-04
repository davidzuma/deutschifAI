import streamlit as st
from gtts import gTTS

from utils.database import get_names_and_definitions_df, insert_data
from utils.generation import generate_description_and_examples

# Streamlit app
st.title("Wortschatz 📖")

# Generate button
name = st.text_input("Neu Wort")


if st.button("Einfügen"):
    if name:
        generated_text = generate_description_and_examples(name)
        # TODO: Move to utils
        try:
            wort = generated_text.split("Wort:")[1].split("Beschreibung:")[0]
            st.session_state.wort = wort
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
    st.markdown(f"**Beschreibung**: {beschreibung}")
    st.markdown(f"**Beispiel**: {beispiele}")
    st.markdown(f"**Ins Englische**: {englische}")

    def text_to_speech(text, lang="de"):
        tts = gTTS(text=text, lang=lang)
        tts.save("german_speech.mp3")
        return "german_speech.mp3"

    # Convert text to speech when button is clicked

    if st.session_state.wort:
        st.markdown("**Die Aussprache** 🔊:")
        audio_file = text_to_speech(st.session_state.wort)
        st.audio(audio_file, format="audio/mp3")

st.subheader("Aktueller Wortschatz")
names_and_definitions_df = get_names_and_definitions_df()

if not names_and_definitions_df.empty:
    names_and_definitions_df.index = names_and_definitions_df["Wort"]
    st.table(names_and_definitions_df["Beschreibung"])
else:
    st.info("No data available in the database.")
