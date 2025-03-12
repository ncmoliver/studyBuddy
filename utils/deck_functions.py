import os
import json

# Define storage path for saved decks
DECKS_FOLDER = "flashcard_decks"
os.makedirs(DECKS_FOLDER, exist_ok=True)

# Function to load existing decks
def load_decks():
    decks = {}
    for file in os.listdir(DECKS_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(DECKS_FOLDER, file), "r") as f:
                decks[file.replace(".json", "")] = json.load(f)
    return decks


# Function to save a deck
def save_deck(deck_name, flashcards):
    """
    Saves the updated flashcard deck to JSON.
    Deletes the file if the deck is empty.
    """
    deck_path = os.path.join(DECKS_FOLDER, f"{deck_name}.json")
    if flashcards:
        with open(deck_path, "w") as f:
            json.dump(flashcards, f)
    else:
        os.remove(deck_path)  # Delete file if no flashcards remain

# Function to delete a deck
def delete_deck(deck_name):
    file_path = os.path.join(DECKS_FOLDER, f"{deck_name}.json")
    if os.path.exists(file_path):
        os.remove(file_path)