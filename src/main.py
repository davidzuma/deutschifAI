import os

import streamlit as st

from nav.account import login, logout
from nav.multiple_choice import multiple_choice_game
from nav.translations import english_translation_game
from utils.constans import DATA_PATH

LOGO = os.path.join(DATA_PATH, "images", "logo.png")
st.set_page_config(
    page_title="DeutschifAI", page_icon=":material/airline_seat_flat_angled:"
)
st.logo(LOGO, icon_image=LOGO)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
vocabulary = st.Page("nav/vocabulary.py", title="Wortschatz", icon=":material/school:")
translations = st.Page(
    english_translation_game, title="Ausbildung", icon=":material/fitness_center:"
)
multiple_choice = st.Page(
    multiple_choice_game, title="Mehrfachauswahl", icon=":material/description:"
)


if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Learning": [vocabulary],
            "Practicing": [translations, multiple_choice],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
