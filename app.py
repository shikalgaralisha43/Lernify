import streamlit as st
from google import genai
import PIL.Image
import json
import os

# ============================================================
# API SETUP
# ============================================================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL = "gemini-3.6-flash"

# ============================================================
# TOPIC DATABASE
# ============================================================
topic_database = {
    "School (9th-12th)": {
        "Physics": ["Motion", "Force & Laws", "Electricity", "Optics", "Waves"],
        "Chemistry": ["Atoms & Molecules", "Chemical Reactions", "Periodic Table", "Organic Chemistry Basics"],
        "Maths": ["Algebra", "Trigonometry", "Calculus Basics", "Probability"],
    },
    "B.Tech - 1st Year": {
        "Engineering Mathematics": ["Matrices", "Calculus", "Differential Equations", "Vectors"],
        "Physics": ["Mechanics", "Optics", "Electromagnetism"],
        "Basic Electrical": ["Circuits", "Ohm's Law", "AC-DC Fundamentals"],
    },
    "B.Tech - 2nd Year": {
        "Data Structures": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs"],
        "Operating Systems": ["Process Management", "Memory Management", "Scheduling", "Deadlocks"],
        "Discrete Mathematics": ["Set Theory", "Graph Theory", "Logic"],
        "Database Management": ["SQL Basics", "Normalization", "ER Diagrams"],
    },
    "B.Tech - 3rd Year (AI/ML)": {
        "Machine Learning": ["Linear Regression", "Logistic Regression", "Decision Trees", "SVM", "K-Means Clustering", "Overfitting & Underfitting"],
        "Deep Learning": ["Neural Networks Basics", "Backpropagation", "CNN", "RNN", "Activation Functions"],
        "Statistics for AI": ["Probability Distributions", "Hypothesis Testing", "Bayes Theorem"],
        "Computer Networks": ["OSI Model", "TCP/IP", "Routing"],
    },
    "B.Tech - 4th Year (AI/ML)": {
        "Advanced ML": ["Ensemble Methods", "Random Forest", "XGBoost", "Transfer Learning"],
        "NLP": ["Tokenization", "Word Embeddings", "Transformers", "Attention Mechanism"],
        "Computer Vision": ["Image Processing", "Object Detection", "Image Segmentation"],
        "AI Ethics & Deployment": ["Bias in AI", "Model Deployment", "MLOps Basics"],
    },
}

# ============================================================
# CORE AI FUNCTIONS
# ============================================================

def explain_image(image, language="Hindi"):
    prompt = f"""You are a friendly engineering senior explaining a concept to your junior.
Look at this diagram/note and explain it:
- In {language} (the casual way students actually talk)
- Using one real-life analogy
- In 3-4 lines, keep it short
"""
    response = client.models.generate_content(model=MODEL, contents=[image, prompt])
    return response.text


def generate_quiz(explanation_text, language="Hindi"):
    prompt = f"""Here is an explanation of an engineering concept:

{explanation_text}

Based on this explanation, create ONE simple multiple-choice question in {language}.
Reply with ONLY JSON, exactly like this (no extra text):

{{
  "question": "question here",
  "options": ["option A", "option B", "option C", "option D"],
  "correct_answer": "the correct option here (must exactly match one of the options)"
}}
"""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def reexplain_simpler(original_explanation, language="Hindi"):
    prompt = f"""This explanation was given to a student earlier:

{original_explanation}

The student got the quiz question wrong, meaning the concept didn't click.
Explain the SAME concept again using a COMPLETELY DIFFERENT analogy (don't repeat the earlier one).
Reply in {language} only, 3-4 lines, make it even simpler."""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text


def get_study_path(level, subject, language="Hindi"):
    topics = topic_database[level][subject]
    topics_str = ", ".join(topics)
    prompt = f"""These are a student's topics for {subject}: {topics_str}

Arrange them in a logical study order (what's needed to understand first should come first).
For each topic, give ONE line explaining why it's in that position.
Reply in {language}.

Format:
1. [Topic Name] - [one line reason]
2. [Topic Name] - [one line reason]
...
"""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text


# ============================================================
# PAGE CONFIG + STYLING
# ============================================================
st.set_page_config(page_title="Lernify", page_icon="📚", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: #FAF8F3;
    }

    .hero-wrap {
        display: flex; align-items: center; justify-content: center;
        gap: 3rem; padding: 2rem 1rem 3rem 1rem; flex-wrap: wrap;
    }
    .hero-text { max-width: 480px; }
    .eyebrow {
        color: #3C6E47; font-weight: 700; letter-spacing: 2px;
        font-size: 0.8rem; text-transform: uppercase;
    }
    .hero-title {
        font-family: 'Poppins', sans-serif; font-size: 3.2rem;
        font-weight: 800; color: #1F2937; line-height: 1.1; margin: 0.5rem 0;
    }
    .hero-title span { color: #3C6E47; }
    .hero-subtitle { color: #4B5563; font-size: 1.05rem; line-height: 1.6; }

    .phone {
        width: 260px; background: linear-gradient(160deg, #3C6E47, #6FA86F);
        border-radius: 36px; padding: 14px;
        box-shadow: 0 25px 60px rgba(60,110,71,0.25);
    }
    .phone-screen {
        background: #FFFFFF;
        border-radius: 24px; padding: 1.2rem 1rem; min-height: 400px;
    }
    .scan-frame { border: 2px dashed #3C6E47; border-radius: 14px; height: 160px; margin-top: 1.5rem; }
    .speech-bubble {
        background: #EAF3EA; color: #1F2937; border-radius: 14px;
        padding: 0.8rem 1rem; font-size: 0.8rem; font-weight: 500; margin-top: 1.2rem;
        border: 1px solid #CFE3CF;
    }
    .phone-label { color: #1F2937; font-weight: 700; font-size: 0.85rem; text-align: center; }

    .feature-card {
        background: #FFFFFF; border: 1px solid #E5E0D5;
        border-radius: 18px; padding: 1.5rem; text-align: center; height: 100%;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }
    .feature-card:hover { transform: translateY(-4px); }
    .feature-icon { font-size: 2.3rem; }
    .feature-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0; color: #1F2937; }
    .feature-desc { color: #6B7280; font-size: 0.88rem; }

    div.stButton > button {
        background: #3C6E47; color: #FFFFFF; border: none; border-radius: 12px;
        padding: 0.7rem 1.8rem; font-weight: 700; width: 100%;
    }
    div.stButton > button:hover { background: #2F5738; }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px; padding: 12px 24px; font-weight: 600;
        background: #FFFFFF; border: 1px solid #E5E0D5; color: #1F2937;
    }

    section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E5E0D5; }

    div[data-testid="stExpander"] {
        border-radius: 14px; border: 1px solid #E5E0D5; background: #FFFFFF;
    }
    .answer-box {
        background: #FFFFFF; border: 1px solid #E5E0D5; border-radius: 14px;
        padding: 1.2rem; margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-text">
        <p class="eyebrow">Built for Tier-2/3 India</p>
        <p class="hero-title">Engineering, explained in <span>your language.</span></p>
        <p class="hero-subtitle">Snap a photo of any diagram or note — Lernify explains it with a real-life analogy, in Hindi or English, then quizzes you to make sure it stuck.</p>
    </div>
    <div class="phone">
        <div class="phone-screen">
            <p class="phone-label">📚 Lernify</p>
            <div class="scan-frame"></div>
            <div class="speech-bubble">"Socho voltage matlab paani ka pressure hai pipe mein..." 💡</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    language = st.selectbox("🌐 Choose language", ["Hindi", "English"])
    st.markdown("---")
    st.markdown("💡 **How it works**")
    st.caption("1. Snap a photo of your diagram or notes\n\n2. Get a fun, relatable explanation\n\n3. Test yourself with a quick quiz")

# ============================================================
# FEATURE CARDS
# ============================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="feature-card"><div class="feature-icon">📸</div><div class="feature-title">Snap & Explain</div><div class="feature-desc">Upload a diagram, get an analogy.</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-card"><div class="feature-icon">🧠</div><div class="feature-title">Doubt-to-Quiz</div><div class="feature-desc">Test yourself instantly.</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-card"><div class="feature-icon">🗺️</div><div class="feature-title">Study Path</div><div class="feature-desc">Smartest topic order.</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INIT
# ============================================================
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "reexplained" not in st.session_state:
    st.session_state.reexplained = None

# ============================================================
# MAIN TABS
# ============================================================
tab1, tab2 = st.tabs(["📸  Snap & Explain", "🗺️  Study Path"])

with tab1:
    st.markdown("#### Upload a photo of your diagram or note")
    st.caption("Get an instant, easy-to-understand explanation with a real-life analogy — then a quick quiz to check it stuck.")

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = PIL.Image.open(uploaded_file)
        st.image(image, width=280)

        if st.button("✨ Explain this"):
            with st.spinner("Reading your diagram..."):
                st.session_state.explanation = explain_image(image, language=language)
                st.session_state.quiz = generate_quiz(st.session_state.explanation, language=language)
                st.session_state.answered = False
                st.session_state.reexplained = None

    if st.session_state.explanation:
        st.markdown(f'<div class="answer-box">{st.session_state.explanation}</div>', unsafe_allow_html=True)

        if st.session_state.quiz:
            st.markdown("#### 🧠 Quick check")
            quiz = st.session_state.quiz
            choice = st.radio(quiz["question"], quiz["options"], index=None, key="quiz_choice")

            if st.button("Submit answer") and choice is not None:
                st.session_state.answered = True
                if choice == quiz["correct_answer"]:
                    st.success("✅ Correct! Great job.")
                    st.session_state.reexplained = None
                else:
                    st.error(f"❌ Not quite. Correct answer: {quiz['correct_answer']}")
                    with st.spinner("Let's try a different angle..."):
                        st.session_state.reexplained = reexplain_simpler(st.session_state.explanation, language=language)

            if st.session_state.reexplained:
                st.markdown("#### 🔄 Here's another way to think about it")
                st.markdown(f'<div class="answer-box">{st.session_state.reexplained}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("#### Get your personalized study path")
    st.caption("Pick your level and subject — we'll tell you the smartest order to study.")

    level = st.selectbox("Your level", list(topic_database.keys()))
    subject = st.selectbox("Subject", list(topic_database[level].keys()))

    if st.button("📋 Generate my study path"):
        with st.spinner("Planning your path..."):
            path = get_study_path(level, subject, language=language)
        st.markdown(f'<div class="answer-box">{path}</div>', unsafe_allow_html=True)
