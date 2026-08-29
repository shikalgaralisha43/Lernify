# 📚 Lernify

**Engineering, explained in your own language.**

Lernify is an AI-powered study companion built for Tier-2/3 India, where engineering
students are fluent in Hindi or a regional language but their textbooks and lectures
are in English. Snap a photo of any diagram or note, and Lernify explains it with a
real-life analogy in Hindi or English — then quizzes you to make sure it stuck.

## Features

- **📸 Snap & Explain** — Upload a photo of a diagram, formula, or handwritten note.
  Gemini reads it and explains the concept using a relatable, everyday analogy.
- **🧠 Doubt-to-Quiz Loop** — After every explanation, answer a quick quiz question.
  Get it wrong, and Lernify explains the same concept again with a *different*
  analogy — no repeated explanations.
- **🗺️ Personalized Study Path** — Pick your level (9th standard through B.Tech
  4th year, with deep AI/ML coverage) and subject. Lernify suggests the smartest
  order to study your topics, with reasons.
- **🌐 Language choice** — Every explanation, quiz, and study path can be generated
  in Hindi or English.

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini API (`gemini-3.6-flash`) — vision + text generation
- **Language**: Python

## Setup

1. Clone this repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

3. Set it as an environment variable:
   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Why Lernify

Most AI study tools translate word-for-word, which loses meaning. Lernify explains
concepts the way a senior would to a junior — with an analogy from everyday life —
so the *idea* transfers, not just the vocabulary.

Built for **Hyperbloom Hacks — September 2026**.
