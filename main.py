import streamlit as st
from openai import OpenAI
import json
import os
import random
from utils.deck_functions import load_decks, save_deck, delete_deck
from utils.quiz_functions import generate_mcq_options, check_answer_with_openai

# OpenAI API Key (Make sure to set this securely)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# Load saved flashcard decks
decks = load_decks()

# Streamlit UI
st.title("📚 Flashcard Creator & Quiz App")

# Sidebar Navigation
option = st.sidebar.radio("Choose an option", ["Create Flashcards", "View Decks", "Test Yourself", "Practice Multiple Choice", "Delete Deck"])

# ---------------------- CREATE FLASHCARDS ----------------------
if option == "Create Flashcards":
    st.subheader("✏️ Create a New Flashcard Deck")

    deck_name = st.text_input("Enter Deck Name:")
    question = st.text_area("Enter Question:")
    answer = st.text_area("Enter Answer:")

    if st.button("Add Flashcard"):
        if deck_name and question and answer:
            if deck_name not in decks:
                decks[deck_name] = []
            decks[deck_name].append({"question": question, "answer": answer})
            save_deck(deck_name, decks[deck_name])
            st.success(f"Flashcard added to '{deck_name}'!")
        else:
            st.warning("Please enter a deck name, question, and answer.")

# ---------------------- VIEW DECKS (WITH DELETE FUNCTIONALITY) ----------------------
elif option == "View Decks":
    st.subheader("📂 View & Manage Flashcard Decks")

    if decks:
        selected_deck = st.selectbox("Select a deck", list(decks.keys()))

        if selected_deck:
            st.write(f"### {selected_deck} Deck")
            updated_flashcards = decks[selected_deck].copy()

            for i, flashcard in enumerate(updated_flashcards):
                with st.expander(f"Flashcard {i+1}"):
                    st.write(f"**Q:** {flashcard['question']}")
                    st.write(f"**A:** {flashcard['answer']}")

                    # Button to delete a specific flashcard
                    if st.button(f"🗑️ Delete Flashcard {i+1}", key=f"del_{selected_deck}_{i}"):
                        decks[selected_deck].remove(flashcard)
                        save_deck(selected_deck, decks[selected_deck])
                        st.rerun()  # Refresh the UI after deletion

            # Button to delete the entire deck
            if st.button(f"🗑️ Delete Entire '{selected_deck}' Deck", key=f"del_deck_{selected_deck}"):
                delete_deck(selected_deck)
                decks.pop(selected_deck, None)
                st.rerun() # Refresh UI after deletion
    else:
        st.info("No decks available. Create one in the 'Create Flashcards' tab.")
# ---------------------- TEST YOURSELF ----------------------
elif option == "Test Yourself":
    st.subheader("📝 Test Yourself on a Flashcard Deck")

    if decks:
        selected_deck = st.selectbox("Select a deck to test", list(decks.keys()))

        num_questions = st.radio("How many questions?", [5, 10])

        if selected_deck:
            flashcards = decks[selected_deck]

            if flashcards:
                # Initialize session state for quiz progress
                if "quiz_active" not in st.session_state:
                    st.session_state.quiz_active = False
                    st.session_state.current_question = 0
                    st.session_state.selected_flashcards = []
                    st.session_state.scores = []
                    st.session_state.show_feedback = False
                    st.session_state.feedback = ""

                # Start the quiz
                if not st.session_state.quiz_active:
                    st.session_state.selected_flashcards = random.sample(flashcards, min(num_questions, len(flashcards)))
                    st.session_state.current_question = 0
                    st.session_state.scores = []
                    st.session_state.quiz_active = True
                    st.session_state.show_feedback = False
                    st.session_state.feedback = ""
                    st.rerun()

                # Get current question
                if st.session_state.current_question < len(st.session_state.selected_flashcards):
                    flashcard = st.session_state.selected_flashcards[st.session_state.current_question]
                    st.markdown(f"## **Q{st.session_state.current_question + 1}:** {flashcard['question']}")
                    user_answer = st.text_input("Your Answer:", key=f"answer_{st.session_state.current_question}")

                    # Show feedback only if the user has submitted an answer
                    if st.button("Submit Answer", key=f"submit_{st.session_state.current_question}"):
                        feedback = check_answer_with_openai(flashcard['question'], user_answer, flashcard['answer'])

                        # Extract correctness percentage
                        correctness_percentage = 0
                        for line in feedback.split("\n"):
                            if line.startswith("Correctness:"):
                                correctness_percentage = int(line.replace("Correctness:", "").strip().replace("%", ""))
                        
                        # Save score and feedback
                        st.session_state.scores.append(correctness_percentage)
                        st.session_state.feedback = feedback
                        st.session_state.show_feedback = True
                        st.rerun()

                    # Display feedback after submission
                    if st.session_state.show_feedback:
                        st.write(st.session_state.feedback)

                        # Button to move to next question
                        if st.button("Next Question"):
                            st.session_state.current_question += 1
                            st.session_state.show_feedback = False
                            st.session_state.feedback = ""
                            st.rerun()

                else:
                    # Quiz Completed - Calculate final score
                    avg_score = sum(st.session_state.scores) / len(st.session_state.scores)

                    # Determine Grade
                    if avg_score >= 90:
                        grade = "A"
                    elif avg_score >= 80:
                        grade = "B"
                    elif avg_score >= 70:
                        grade = "C"
                    elif avg_score >= 60:
                        grade = "D"
                    else:
                        grade = "F"

                    st.write(f"### Quiz Completed! Your Final Score: {avg_score:.2f}% ({grade})")

                    # Reset Quiz
                    if st.button("Restart Quiz"):
                        st.session_state.quiz_active = False
                        st.rerun()
    else:
        st.info("No decks available. Create one in the 'Create Flashcards' tab.")


# ---------------------- TEST YOURSELF WITH MCQ ----------------------
elif option == "Practice Multiple Choice":
    st.subheader("📝 Practice Multiple Choice Questions")

    if decks:
        selected_deck = st.selectbox("Select a deck to practice", list(decks.keys()))

        difficulty = st.radio("Select Difficulty", ["Easy", "Medium", "Hard"])

        if selected_deck:
            flashcards = decks[selected_deck]

            if flashcards:
                # Initialize session state
                if "quiz_active" not in st.session_state:
                    st.session_state.quiz_active = False
                    st.session_state.current_question = 0
                    st.session_state.selected_flashcards = []
                    st.session_state.scores = []
                    st.session_state.show_feedback = False
                    st.session_state.feedback = ""
                    st.session_state.answer_choices = []

                if not st.session_state.quiz_active:
                    st.session_state.selected_flashcards = random.sample(flashcards, min(5, len(flashcards)))
                    st.session_state.current_question = 0
                    st.session_state.scores = []
                    st.session_state.quiz_active = True
                    st.session_state.show_feedback = False
                    st.session_state.feedback = ""
                    st.session_state.answer_choices = []
                    st.rerun()

                # Get the current question
                if st.session_state.current_question < len(st.session_state.selected_flashcards):
                    flashcard = st.session_state.selected_flashcards[st.session_state.current_question]
                    with st.container():
                        st.markdown(f"## **Q{st.session_state.current_question + 1}:** {flashcard['question']}", unsafe_allow_html=True)

                        # Generate unique MCQ options
                        options = generate_mcq_options(flashcard["answer"], flashcards)
                        st.session_state.answer_choices = options

                        user_answer = st.selectbox("Select an Answer:", options, key=f"answer_{st.session_state.current_question}")

                    if st.button("Submit Answer", key=f"submit_{st.session_state.current_question}"):
                        feedback = check_answer_with_openai(flashcard['question'], user_answer, flashcard['answer'], api_key=OPENAI_API_KEY)

                        # Extract correctness percentage
                        correctness_percentage = 0
                        for line in feedback.split("\n"):
                            if line.startswith("Correctness:"):
                                correctness_percentage = int(line.replace("Correctness:", "").strip().replace("%", ""))
                        
                        st.session_state.scores.append(correctness_percentage)
                        st.session_state.feedback = feedback
                        st.session_state.show_feedback = True
                        st.rerun()

                    # Display feedback after submission
                    if st.session_state.show_feedback:
                        st.write(st.session_state.feedback)

                        # Button to move to next question
                        if st.button("Next Question"):
                            st.session_state.current_question += 1
                            st.session_state.show_feedback = False
                            st.session_state.feedback = ""
                            st.rerun()

                else:
                    # Quiz Completed - Calculate final score
                    avg_score = sum(st.session_state.scores) / len(st.session_state.scores)

                    # Determine Grade
                    if avg_score >= 90:
                        grade = "A"
                    elif avg_score >= 80:
                        grade = "B"
                    elif avg_score >= 70:
                        grade = "C"
                    elif avg_score >= 60:
                        grade = "D"
                    else:
                        grade = "F"

                    st.write(f"### Quiz Completed! Your Final Score: {avg_score:.2f}% ({grade})")

                    # Reset Quiz
                    if st.button("Restart Quiz"):
                        st.session_state.quiz_active = False
                        st.rerun()

    else:
        st.info("No decks available. Create one in the 'Create Flashcards' tab.")



# ---------------------- DELETE DECK ----------------------
elif option == "Delete Deck":
    st.subheader("🗑️ Delete a Flashcard Deck")

    if decks:
        selected_deck = st.selectbox("Select a deck to delete", list(decks.keys()))
        if st.button(f"Delete '{selected_deck}'"):
            delete_deck(selected_deck)
            decks.pop(selected_deck, None)
            st.success(f"Deleted deck '{selected_deck}' successfully!")
    else:
        st.info("No decks available.")

