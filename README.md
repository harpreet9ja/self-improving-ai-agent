# 🤖 AI Persona Chatbot (Harpreet Singh Walia)

This project is a **personal AI chatbot** that represents _Harpreet Singh Walia_ on a website.
It answers questions about career, skills, and experience using:

- 📄 Resume (PDF)
- 📝 Summary file
- 🤖 LLMs (OpenAI + Groq)
- 🧠 Self-evaluation loop for better responses
- 💬 Gradio UI for interaction

---

## 🚀 Features

- **Persona-based responses** (acts as Harpreet)
- **Context-aware answers** using:
  - Resume (PDF parsing via PyPDF)
  - Custom summary file

- **Response evaluation system**
  - Uses LLM to check answer quality
  - Automatically improves bad responses

- **Dual LLM setup**
  - OpenAI → primary response + evaluation
  - Groq → fallback/improvement

- **Simple chat UI** using Gradio

---

## 🧱 Tech Stack

- Python
- OpenAI API
- Groq API (LLaMA 3.3)
- Gradio
- PyPDF
- Pydantic
- python-dotenv

---

## 📂 Project Structure

```
.
├── me/
│   ├── Profile.pdf        # Resume / LinkedIn export
│   └── summary.txt       # Short professional summary
├── app.py                # Main application
├── .env                  # API keys (not committed)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd <repo-name>
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If no requirements file:

```bash
pip install openai groq gradio pypdf python-dotenv pydantic
```

---

### 4. Setup environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
```

---

### 5. Add your data

- Place your resume at:

  ```
  me/Profile.pdf
  ```

- Add your summary:

  ```
  me/summary.txt
  ```

---

### 6. Run the app

```bash
python app.py
```

Gradio UI will open in browser 🎉

---

## 🧠 How It Works

### Step 1: Load Context

- Extract text from PDF (resume)
- Load summary file

### Step 2: Generate Response

- OpenAI generates initial answer using persona prompt

### Step 3: Evaluate Response

- LLM checks:
  - professionalism
  - relevance
  - quality

### Step 4: सुधार (Improve)

- If rejected:
  - Feedback is generated
  - Groq LLaMA re-generates better answer

---

## 🔁 Flow Diagram (mental model)

```
User → OpenAI → Evaluator → (Good ✅ → Return)
                           → (Bad ❌ → Groq सुधार → Return)
```

---

## ⚠️ Notes

- Do NOT commit `.env`
- Ensure PDF has extractable text (not scanned)
- Evaluation adds latency but improves quality

---

## 💡 Future Improvements

- Add streaming responses
- Store chat history
- Deploy on cloud (HF Spaces / AWS / Vercel)
- Add voice interface
- Multi-persona support

---

## 👤 Author

**Harpreet Singh Walia**

---

## 🪪 License

MIT License (or your preferred license)
