import streamlit as st
import json
import random

# Load quiz data from JSON file
def load_quiz(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

# Initialize session state on first run
def initialize_session(quiz_data):
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.session_state.quiz = random.sample(quiz_data, len(quiz_data))  # shuffle questions

# Display one question at a time
def run_quiz():
    quiz = st.session_state.quiz
    current_index = st.session_state.current_question
    question_data = quiz[current_index]

    st.markdown(f"**Question {current_index + 1} of {len(quiz)}**")
    st.markdown(f"**{question_data['question']}**")

    user_answer = st.radio("Select your answer:", question_data["options"], key=current_index)

    if st.button("Submit Answer"):
        correct = user_answer == question_data["answer"]
        st.session_state.user_answers.append((question_data["question"], user_answer, question_data["answer"], correct))
        if correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect. The correct answer was: **{question_data['answer']}**")

        if st.session_state.current_question < len(quiz) - 1:
            st.session_state.current_question += 1
        else:
            st.session_state.quiz_complete = True

# Display final results
def show_results():
    st.title("🎉 Quiz Completed!")
    st.write(f"Your score: {st.session_state.score} / {len(st.session_state.quiz)}")

    for q, user_ans, correct_ans, is_correct in st.session_state.user_answers:
        st.markdown(f"**Q:** {q}")
        st.markdown(f"Your Answer: {'✅ ' if is_correct else '❌ '}{user_ans}")
        if not is_correct:
            st.markdown(f"Correct Answer: {correct_ans}")
        st.markdown("---")

    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()