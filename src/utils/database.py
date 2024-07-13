import random
import sqlite3


def create_names_definitions_table():
    conn = sqlite3.connect("vocabulary.db")
    cursor = conn.cursor()
    # Create a table
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
    conn.close()


# Function to insert data into the database
def insert_data(wort, beschreibung, beispiele, englische):
    conn = sqlite3.connect("vocabulary.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO names_definitions (Wort, Beschreibung, Beispiele, Englische) VALUES (?, ?, ?, ?)",
        (wort, beschreibung, beispiele, englische),
    )
    conn.commit()
    conn.close()


def fetch_random_word():
    conn = sqlite3.connect("vocabulary.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Wort, Englische FROM names_definitions ORDER BY RANDOM() LIMIT 1"
    )
    word = cursor.fetchone()
    conn.close()

    if word:
        german_word, english_translation = word
        return (german_word, english_translation)
    else:
        return None


def get_word_and_options():
    # Connect to the SQLite database
    conn = sqlite3.connect("vocabulary.db")
    c = conn.cursor()

    # Get a random word and its correct translation
    c.execute("SELECT Wort, Englische FROM names_definitions ORDER BY RANDOM() LIMIT 1")
    word, correct_translation = c.fetchone()

    # Get 3 incorrect translations
    c.execute(
        "SELECT Englische FROM names_definitions WHERE Wort != ? ORDER BY RANDOM() LIMIT 3",
        (word,),
    )
    incorrect_translations = [row[0] for row in c.fetchall()]

    # Combine all options and shuffle
    options = [correct_translation] + incorrect_translations
    random.shuffle(options)

    # Close the connection
    conn.close()

    return word, correct_translation, options
