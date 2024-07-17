import contextlib
import os
import random

import pandas as pd
import sqlitecloud
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SQLITECLOUD_API_KEY = os.getenv("SQLITECLOUD_API_KEY")


@contextlib.contextmanager
def get_db_connection():
    conn = sqlitecloud.connect(
        f"sqlitecloud://ctemvrrusk.sqlite.cloud:8860?apikey={SQLITECLOUD_API_KEY}"
    )
    db_name = "vocabulary.db"
    conn.execute(f"USE DATABASE {db_name}")
    try:
        yield conn
    finally:
        conn.close()


def create_names_definitions_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS names_definitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Wort TEXT NOT NULL,
            Beschreibung TEXT NOT NULL,
            Beispiele TEXT NOT NULL,
            Englische TEXT NOT NULL
        )
        """
        )
        conn.commit()


def insert_data(wort, beschreibung, beispiele, englische):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO names_definitions (Wort, Beschreibung, Beispiele, Englische) VALUES (?, ?, ?, ?)",
            (wort, beschreibung, beispiele, englische),
        )
        conn.commit()


def fetch_random_word():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Wort, Englische FROM names_definitions ORDER BY RANDOM() LIMIT 1"
        )
        word = cursor.fetchone()

    if word:
        german_word, english_translation = word
        return (german_word, english_translation)
    else:
        return None


def get_word_and_options():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get a random word and its correct translation
        cursor.execute(
            "SELECT Wort, Englische FROM names_definitions ORDER BY RANDOM() LIMIT 1"
        )
        word, correct_translation = cursor.fetchone()

        # Get 3 incorrect translations
        cursor.execute(
            "SELECT Englische FROM names_definitions WHERE Wort != ? ORDER BY RANDOM() LIMIT 3",
            (word,),
        )
        incorrect_translations = [row[0] for row in cursor.fetchall()]

    # Combine all options and shuffle
    options = [correct_translation] + incorrect_translations
    random.shuffle(options)

    return word, correct_translation, options


def get_names_and_definitions_df():
    with get_db_connection() as conn:
        names_and_definitions_df = pd.read_sql("SELECT * FROM names_definitions", conn)
    return names_and_definitions_df
