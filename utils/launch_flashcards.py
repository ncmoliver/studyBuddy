import tkinter as tk
import json

def launch_flashcard_viewer(json_file_path):
    """Launches a Tkinter flashcard app using a JSON file with MCQ format."""
    
    # Load questions from file
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            flashcards = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return

    # Track state
    current_index = [0]  # Use list so it’s mutable in nested functions
    showing_question = [True]

    # Initialize window
    root = tk.Tk()
    root.title("🧠 Flashcard Viewer")
    root.geometry("600x300")
    root.configure(bg="white")

    # Text area for card
    card_text = tk.Label(root, text="", wraplength=500, font=("Helvetica", 18), bg="white", justify="center")
    card_text.pack(expand=True)

    # Update flashcard display
    def show_card():
        card = flashcards[current_index[0]]
        if showing_question[0]:
            card_text.config(text=f"❓ {card['question']}")
        else:
            card_text.config(text=f"✅ {card['answer']}")

    # Flip card (question <-> answer)
    def flip_card(event=None):
        showing_question[0] = not showing_question[0]
        show_card()

    # Next card
    def next_card(event=None):
        if current_index[0] < len(flashcards) - 1:
            current_index[0] += 1
            showing_question[0] = True
            show_card()

    # Previous card
    def prev_card(event=None):
        if current_index[0] > 0:
            current_index[0] -= 1
            showing_question[0] = True
            show_card()

    # Exit
    def exit_flashcards(event=None):
        root.destroy()

    # Key bindings
    root.bind("<space>", flip_card)
    root.bind("<Right>", next_card)
    root.bind("<Left>", prev_card)
    root.bind("<Return>", exit_flashcards)

    # Start with first card
    show_card()
    root.mainloop()
