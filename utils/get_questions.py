import json
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

# Ensure API key is set
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_mcq_from_text_file(text_file_path, num_questions, output_json="mcq_output.json"):
    """
    Uses OpenAI GPT to generate multiple-choice questions from a text file.
    """
    # Step 1: Read file safely
    try:
        with open(text_file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except FileNotFoundError:
        st.error(f"❌ File not found: {text_file_path}")
        return None
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return None

    if not content:
        st.warning("⚠️ Text file is empty.")
        return None

    # Step 2: Prompt
    prompt = f"""
You are a test generator. Based on the following study material, generate exactly {num_questions} multiple-choice questions.

**Requirements:**
- Each question must have exactly four answer choices.
- Provide the correct answer explicitly.
- Format the result as a JSON array using this structure:

[
  {{
    "question": "What is the capital of France?",
    "options": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "Paris"
  }},
  ...
]

**Study Material:** 
{content}
"""

    # Step 3: OpenAI Request
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that generates multiple-choice questions (MCQs) from study material."
    },
    {
        "role": "user",
        "content": f"""
Using the provided study material, generate exactly {num_questions} multiple-choice questions.

⚠️ Strict instructions:
- Each question must include exactly **four** answer choices under `"options"`.
- Include the correct answer under the `"answer"` field as an exact match from the options.
- Do **not** include any additional text or explanation.
- Do **not** use code blocks or markdown formatting (no triple backticks).
- Return the result **only** as a pure JSON array, following this exact structure:

[
  {{
    "question": "What is the capital of France?",
    "options": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "Paris"
  }},
  ...
]

📘 Study Material:
{content}
"""
    }
],
            temperature=0.3,
            max_tokens=3000
        )
    except Exception as e:
        st.error(f"❌ OpenAI API call failed: {e}")
        return None

    # Step 4: Parse JSON response
    message_content = response.choices[0].message.content.strip()
    try:
        mcqs = json.loads(message_content)
    except json.JSONDecodeError as e:
        st.error("❌ Failed to parse response from OpenAI as JSON.")
        st.text_area("🧾 Raw response from OpenAI", message_content, height=300)
        return None

    # Step 5: Save output
    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(mcqs, f, indent=4)
        st.success(f"✅ {len(mcqs)} questions saved to {output_json}")
    except Exception as e:
        st.error(f"❌ Failed to save output: {e}")

    return mcqs