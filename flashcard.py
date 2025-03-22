# flashcards.py
from tkinter import *
import json
import sys

def launch_flashcard_viewer(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        flashcards = json.load(f)

    current_index = [0]
    showing_question = [True]

    root = Tk()
    root.title("Flashcards")
    root.geometry("600x300")
    root.configure(bg="white")

    card_text = Label(root, text="", wraplength=500, font=("Helvetica", 18), bg="white", justify="center")
    card_text.pack(expand=True)

    def show_card():
        card = flashcards[current_index[0]]
        if showing_question[0]:
            card_text.config(text=f"❓ {card['question']}")
        else:
            card_text.config(text=f"✅ {card['answer']}")

    def flip_card(event=None):
        showing_question[0] = not showing_question[0]
        show_card()

    def next_card(event=None):
        if current_index[0] < len(flashcards) - 1:
            current_index[0] += 1
            showing_question[0] = True
            show_card()

    def prev_card(event=None):
        if current_index[0] > 0:
            current_index[0] -= 1
            showing_question[0] = True
            show_card()

    def exit_flashcards(event=None):
        root.destroy()

    root.bind("<space>", flip_card)
    root.bind("<Right>", next_card)
    root.bind("<Left>", prev_card)
    root.bind("<Return>", exit_flashcards)

    show_card()
    root.mainloop()

# Entry point
if __name__ == "__main__":
    json_file_path = sys.argv[1]
    launch_flashcard_viewer(json_file_path)
