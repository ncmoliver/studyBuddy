from openai import OpenAI
import streamlit as st
import random



# Function to query OpenAI for answer validation
@st.cache_data
def check_answer_with_openai(question, user_answer, correct_answer, api_key):
    prompt = f"""
    Question: {question}
    User's Answer: {user_answer}
    Correct Answer: {correct_answer}
    
    Evaluate the response:
    1. If the answer is correct, reply with "✅ Correct!"
    2. If incorrect, explain why it's wrong and provide hints or a brief correction.
    3. Respond in this format:

    Correctness: X%
    Feedback: <short explanation>
    """
    client = OpenAI(api_key = api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a quiz evaluator. Provide correctness percentage and feedback."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content



# Function to generate MCQ answer choices
@st.cache_data
def generate_mcq_options(correct_answer, flashcards, num_choices=4):
    """
    Generate multiple-choice options where one option is the correct answer, 
    and the others are randomly selected from the dataset.
    """
    all_answers = list(set([fc["answer"] for fc in flashcards if fc["answer"] != correct_answer]))  # Avoid duplicate correct answer
    wrong_answers = random.sample(all_answers, min(len(all_answers), num_choices - 1))  # Pick unique wrong answers

    options = wrong_answers + [correct_answer]  # Add correct answer
    random.shuffle(options)  # Shuffle order
    return options

# Function to check answer with OpenAI (provides correctness percentage & feedback)
@st.cache_data
def check_answer_with_openai(question, user_answer, correct_answer, api_key):
    prompt = f"""
    Question: {question}
    User's Answer: {user_answer}
    Correct Answer: {correct_answer}

    Evaluate the user's response:
    1. Provide a correctness percentage (0-100%).
    2. If the answer is incorrect, provide a short explanation and the correct answer.
    3. Respond in this format:

    Correctness: X%
    Feedback: <short explanation>
    """
    client = OpenAI(api_key = api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a quiz evaluator. Provide correctness percentage and feedback."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content