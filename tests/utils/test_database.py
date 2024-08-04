import random
from unittest.mock import Mock, patch

import pytest

from utils.database import get_word_and_options


@pytest.fixture
def mock_db_connection():
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


def test_get_word_and_options(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection

    # Mock the database query results
    mock_cursor.fetchone.return_value = ("Apfel", "apple")
    mock_cursor.fetchall.return_value = [("banana",), ("orange",), ("grape",)]

    # Set a fixed seed for reproducibility
    random.seed(42)

    # Patch the database connection
    with patch("utils.database.get_db_connection") as mock_get_db:
        mock_get_db.return_value.__enter__.return_value = mock_conn

        # Call the function
        word, correct_translation, options = get_word_and_options()

        # Assertions
        assert word == "Apfel"
        assert correct_translation == "apple"
        assert set(options) == set(["apple", "banana", "orange", "grape"])
        assert len(options) == 4
        assert correct_translation in options

        # Check that the database queries were called correctly
        mock_cursor.execute.assert_any_call(
            "SELECT Wort, Englische FROM names_definitions ORDER BY RANDOM() LIMIT 1"
        )
        mock_cursor.execute.assert_any_call(
            "SELECT Englische FROM names_definitions WHERE Wort != ? ORDER BY RANDOM() LIMIT 3",
            ("Apfel",),
        )


def test_get_word_and_options_shuffling(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection

    # Mock the database query results
    mock_cursor.fetchone.return_value = ("Apfel", "apple")
    mock_cursor.fetchall.return_value = [("banana",), ("orange",), ("grape",)]

    # Patch the database connection
    with patch("utils.database.get_db_connection") as mock_get_db:
        mock_get_db.return_value.__enter__.return_value = mock_conn

        # Call the function multiple times
        results = [get_word_and_options() for _ in range(10)]

        # Check that the options are shuffled
        option_orders = [result[2] for result in results]
        assert (
            len(set(tuple(order) for order in option_orders)) > 1
        ), "Options should be shuffled"
