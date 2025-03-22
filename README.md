
# ✨ StudyBuddy AI ✨  
**Turn Your Notes into Smart Study Tools with AI**

---

## 📚 Overview

Welcome to **StudyBuddy AI**, your intelligent companion for transforming **handwritten or computer-based notes** into **interactive, personalized study materials** using the power of AI.

This project combines the accessibility of **Streamlit**, the intelligence of **OpenAI's GPT-4**, and the simplicity of **Tkinter** to build a full-fledged learning toolkit from just your **notes** — no matter how messy or complex.

Whether you're a student, educator, or lifelong learner, StudyBuddy AI makes your learning process smarter, faster, and more engaging.

---

## 🚀 How It Works

### 1. 🖼 Upload Your Study Notes
Upload **images of your handwritten or typed notes** (JPG, PNG, etc.) through the Streamlit interface.

### 2. 🧠 Text Extraction with OpenAI
Each uploaded image is sent to **OpenAI’s GPT-4o** model via a prompt-engineered request. The AI:
- Detects and extracts text content
- Combines all extracted notes into one clean document

### 3. 📝 Automatic Quiz Generation
The full extracted content is then passed through a **second OpenAI prompt**, specifically crafted to:
- Identify key concepts
- Generate **multiple-choice questions (MCQs)** based on the content
- Provide four answer options per question
- Identify and mark the **correct answer**

The result? A beautifully structured **JSON file** that serves as the engine for everything that follows.

### 4. 🔁 Choose Your Learning Mode
Once your questions are generated, StudyBuddy AI offers you multiple ways to study:

#### 🎴 Flashcard Mode (Tkinter)
Launch a **Tkinter-based flashcard app** that:
- Shows one question per card
- Flips to the answer with the spacebar
- Navigate with ⬅️/➡️ arrow keys
- Exit the session with Enter

#### 🧪 Quiz Mode (Streamlit)
Take a **step-by-step multiple-choice test** in your browser with:
- One question per screen
- Instant feedback after submission
- Final score, percentage, and grade

#### 💾 Download Mode
Download your entire quiz set as a `.json` file for sharing, editing, or reusing later.

---

## 🛠 Technologies Used

| Technology     | Purpose                                             |
|----------------|-----------------------------------------------------|
| **Streamlit**  | Web interface and quiz system                       |
| **OpenAI GPT-4o** | Image-to-text and quiz generation using prompt engineering |
| **Tkinter**    | Lightweight GUI for flashcard experience            |
| **Python**     | Backend logic, API calls, and data processing       |
| **JSON**       | Data structure for questions and quiz content       |
| **Pillow (PIL)** | Handling and displaying image content              |

---

## 📁 File Structure

```bash
├── main_app.py              # Streamlit frontend logic
├── flashcards.py            # Tkinter-based flashcard GUI
├── utils/
│   └── openai_utils.py      # Text extraction and quiz generation
├── your_test.json           # Output: AI-generated questions
├── requirements.txt         # All dependencies
└── README.md                # You're reading it!
```

---

## 🎓 Use Case Scenarios

- **Students** preparing for exams from messy notebooks
- **Teachers** generating quizzes from worksheets or lectures
- **Lifelong learners** organizing study material visually
- **Remote educators** offering digital flashcard sets to their students

---

## 🧪 Example Workflow

1. **Upload Note Images**
   - E.g., `biology_notes.jpg`, `chapter1_summary.png`

2. **Generate MCQs**
   - AI reads, understands, and transforms content

3. **Choose Learning Mode**
   - Flashcards? Testing? Download? Your choice.

4. **Learn Smarter**
   - Track your score, retry incorrect answers, and boost retention.

---

## 💡 Future Enhancements

- 📤 Export scores to PDF report
- 🗃 Deck builder with tagging by subject/topic
- 🎙️ Voice-enabled flashcards
- 📱 Mobile compatibility (Streamlit Cloud/PWA)
- 🔒 Authentication and profile-based question saving

---

## 🧰 Installation & Setup

```bash
git clone https://github.com/yourusername/studybuddy-ai.git
cd studybuddy-ai
pip install -r requirements.txt
streamlit run main_app.py
```

Make sure to set your **OpenAI API key** as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

---

## 🧠 Sample JSON Format

```json
[
  {
    "question": "Which type of media is used to transmit data over a network?",
    "options": ["Copper", "Plastic", "Wood", "Glass"],
    "answer": "Copper"
  }
]
```

---

## ✨ Credits

- 🤖 Powered by [OpenAI](https://openai.com/)
- 💡 Interface by [Streamlit](https://streamlit.io/)
- 🧪 Flashcards built with 💛 using Tkinter

---

## 🧩 Contribute

Want to enhance the flashcards? Add spaced repetition? Improve feedback?  
We welcome contributions! Fork the repo and create a pull request 🚀

---

## 🛡 License

MIT License – free to use and modify, just give credit where due.

---

## 🙌 Final Thoughts

**StudyBuddy AI** isn’t just a tool—it’s a revolution in how we study.  
From handwritten notes to interactive learning in seconds.

Make your notes work for you.  
**Study smart. Learn better. Win exams.**
