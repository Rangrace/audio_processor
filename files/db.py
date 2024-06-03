# Imports
from nltk.corpus import words
import spacy
import sqlite3
import json

# Load Spacy model
nlp = spacy.load(u'en_core_web_md')

# Get wordlist
wordlist = words.words()


class db_connection_context_manager:
    """Context manager to handle the database connection"""

    def __enter__(self):
        self.connection = sqlite3.connect('speech_training.sqlite')
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()


def transfer_to_db(values: dict):
    """The function is used to transfer information to the database"""

    # Creating a spacy.tokens.Doc instance
    doc = nlp(values["user_content"])

    # Iterates through doc and saves all tokens as strings in a list as lowercase
    tokens = [token.text.lower() for token in doc]

    # If a token is alphanumeric and not in the wordlist, it's saved in a list
    tokens_not_in_wordlist = [token for token in tokens if token.isalnum() and token not in wordlist]

    # Json formatted strings from the tokens and tokens_not_in_wordlist lists
    tokens_json = json.dumps(tokens)
    tokens_not_in_wordlist_json = json.dumps(tokens_not_in_wordlist)

    with db_connection_context_manager() as connection:
        # Creating a cursor object to be able to execute the sql query
        cursor = connection.cursor()

        # Insert the data into the database table
        cursor.execute("""
                    INSERT INTO prompts (date, user_content, tokens, tokens_not_in_wordlist)
                    VALUES (?, ?, ?, ?)
                """, (values["date"], values["user_content"], tokens_json, tokens_not_in_wordlist_json))

        # Send
        connection.commit()



