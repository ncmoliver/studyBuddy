import streamlit as st
from utils.get_questions import generate_mcq_from_text_file
from utils.launch_flashcards import launch_flashcard_viewer
from utils.json_to_quiz import load_quiz, initialize_session, run_quiz, show_results
from utils.image_to_text import extract_and_save_text_from_images
import subprocess
import sys


######################### Streamlit App #########################


st.title("📘 Flashcard Generator")
uploaded_images = st.sidebar.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_images and st.sidebar.button("Extract & Save Text"):
    output_path = extract_and_save_text_from_images(uploaded_images, "notecard_text.txt")
    
    with open(output_path, "r", encoding="utf-8") as f:
        extracted_text = f.read()


num_questions = st.number_input("Number of questions to generate", min_value=1, max_value=50, value=10)

if st.button("Generate MCQs"):
    mcq_output = generate_mcq_from_text_file("notecard_text.txt", num_questions)
else:
    mcq_output = None

st.subheader("🧠 Let's Start Learning")
options = ["", "Download JSON Questions", "Flashcards", "Test Yourself"]
user_choice = st.selectbox("Choose an option", options=options)
if user_choice == "Download JSON Questions":
    file_name = "mcq_output.json"
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            file_contents = f.read()

        st.download_button(
            label="📥 Download MCQs",
            data=file_contents,  # ✅ actual content of the file
            file_name=file_name,
            mime="application/json"
        )
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_name}")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

elif user_choice == "Flashcards":
    st.subheader("Flashcards")
    python_cmd = sys.executable  # gets the path to current Python interpreter
    subprocess.Popen([python_cmd, "flashcard.py", "mcq_output.json"], bufsize=1)
    st.success("✅ Flashcard viewer launched!")

elif user_choice == "Test Yourself":
    load_quiz("mcq_output.json")
    initialize_session(mcq_output)
    run_quiz()
    if "quiz_complete" in st.session_state and st.session_state.quiz_complete:
        show_results()
        st.session_state.quiz_complete = False
    else:
        st.warning("Please complete the quiz before viewing results.")


