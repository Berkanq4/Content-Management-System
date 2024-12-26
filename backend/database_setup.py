import requests
from models import db, WordPhrase
import json

def load_initial_data():
    try:
        with open('sample_data.json', 'r', encoding='utf-8') as f:  # Open local JSON file
                data = json.load(f)

        for entry in data:
            word = WordPhrase(
                word=entry['word'],
                translation=entry['translation'],
                example_sentence=entry.get('example_sentence', "")
            )
            db.session.add(word)
        db.session.commit()
    except FileNotFoundError:
        print("Error: sample_data.json not found. Make sure the file exists in the correct directory.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e: # Catching other potential errors
        print(f"An unexpected error occurred: {e}")
