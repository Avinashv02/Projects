import streamlit as st
from pymongo import MongoClient
import requests
from datetime import datetime
import re

# --- Configuration ---
OPENROUTER_API_KEY = "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"
MONGO_URI = "mongodb+srv://avinashv02official:9891706066Avi@cluster0.yhfge.mongodb.net/?retryWrites=false&tls=true"

# MongoDB Setup
client = MongoClient(MONGO_URI)
db = client["feedback_database"]
feedback_collection = db["feedbacks"]

# Page Config
st.set_page_config(page_title="Lumina AI", layout="wide", page_icon="✨")

# --- Styles ---
def load_styles(theme, themes):
    if themes == "Aurora":
        st.markdown(Aurora_theme_css, unsafe_allow_html=True)
    elif themes == "Cosmic":
        st.markdown(cosmic_theme_css, unsafe_allow_html=True)
    else:
        st.markdown(nebula_theme_css, unsafe_allow_html=True)

# Custom CSS for each theme with hover effects for buttons
Aurora_theme_css = """
    <style>
    .main-header {
        color: #D0F0FF;
        text-align: center;
        font-family: 'Roboto', sans-serif;
        font-size: 2em;
        text-shadow: 0 0 10px rgba(80, 200, 255, 0.7);
    }

    .stButton > button {
        background: linear-gradient(90deg, #1CB5E0, #000851);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 8px 24px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(28, 181, 224, 0.6);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        transform: scale(1.08);
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.8);
    }

    .response-text {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid #4FC3F7;
        color: #E0F7FA;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(79, 195, 247, 0.5);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(31, 64, 55, 0.9), rgba(10, 25, 47, 0.9));
    }

    .stTextInput > div > input {
        background-color: #1c1c1c;
        border: 2px solid #4FC3F7;
        border-radius: 8px;
        color: #E0F7FA;
        padding: 8px;
        font-size: 1em;
    }
    </style>
"""

cosmic_theme_css = """
    <style>
    .main-header {
        color: #FF6EC7;
        text-align: center;
        font-family: 'Roboto', sans-serif;
        font-size: 2em;
        text-shadow: 0 0 15px rgba(255, 110, 199, 0.8);
    }

    .stButton > button {
        background: linear-gradient(90deg, #5C258D, #4389A2);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(92, 37, 141, 0.6);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #8E2DE2, #4A00E0);
        transform: scale(1.1);
        box-shadow: 0 0 18px rgba(142, 45, 226, 0.9);
    }

    .response-text {
        background: rgba(20, 20, 20, 0.85);
        border: 1px solid #5C258D;
        color: #F0F0F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(68, 0, 255, 0.4);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
        color: #FFFFFF;
    }

    .stTextInput > div > input {
        background-color: #1c1c1c;
        border: 2px solid #5C258D;
        border-radius: 8px;
        color: #FFFFFF;
        padding: 10px;
        font-size: 1em;
    }
    </style>
"""

nebula_theme_css = """
    <style>
    .main-header {
        color: #FF6EFF;
        text-align: center;
        font-family: 'Roboto', sans-serif;
        font-size: 2em;
        text-shadow: 0 0 15px rgba(255, 110, 255, 0.8);
    }

    .stButton > button {
        background: linear-gradient(90deg, #8338ec, #3a86ff);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 0 12px rgba(131, 56, 236, 0.6);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #E0E0E0, #FF6EFF);
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.8);
    }

    .response-text {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid #FF6EFF;
        color: #F0F0F0;
        padding: 20px;
        border-radius: 12px;
        backdrop-filter: blur(8px);
        box-shadow: 0 0 20px rgba(255, 110, 255, 0.3);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #3a0ca3, #240046);
        color: #FFFFFF;
    }

    .stTextInput > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid #8338ec;
        border-radius: 10px;
        color: #FFFFFF;
        padding: 10px;
        font-size: 1em;
    }
    </style>
"""

# --- Utilities ---
def get_openrouter_response(question):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Lumina AI",
    }
    data = {
        "model": "anthropic/claude-3-haiku",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
    
# --- Chat Components ---
def initialize_session_state():
    defaults = {
        "chat_history": [],
        "submitted": False,
        "input_value": "",
        "temp_input": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def handle_input_submission():
    if st.session_state.temp_input:
        st.session_state.input_value = st.session_state.temp_input
        st.session_state.submitted = True
        st.session_state.temp_input = ""

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.input_value = ""
    st.session_state.submitted = False

def render_chat_interface():
    initialize_session_state()

    # We'll create a single container for the entire chat interface
    with st.container():
        st.markdown("<h3>Engage with Lumina</h3>", unsafe_allow_html=True)
        
        # Using a container to wrap all input elements
        with st.container():
            # Input field
            st.text_input("Ask away...", key="temp_input", on_change=handle_input_submission)
            
            # Buttons in columns
            col1, col2 = st.columns(2)
            with col1:
                st.button("Submit", on_click=handle_input_submission)
            with col2:
                st.button("Clear Chat", on_click=clear_chat)

    # Process Input
    if st.session_state.submitted and st.session_state.input_value:
        process_user_input()

    # Chat History
    display_chat_history()

def process_user_input():
    user_input = st.session_state.input_value
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Processing..."):
        question_lower = user_input.lower()
        if "who" in question_lower and any(p in question_lower for p in ["developed", "created", "made", "you"]):
            response = (
                "I am <span style='font-weight: bold;'>Lumina</span>, an AI built for brilliance. "
                "Created by Avinash Verma from DTU. Connect with him on "
                "<a href='https://www.linkedin.com/in/avinash-verma-584655261/'>LinkedIn</a>."
            )
        elif "time" in question_lower:
            response = f"Current time: {datetime.now().strftime('%I:%M:%S %p')} (UTC)"
        elif "how are you" in question_lower:
            response = "I'm a digital entity, thriving on code! How can I help you today?"
        else:
            response = get_openrouter_response(user_input) or "Sorry, something went wrong."
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.session_state.submitted = False
    st.session_state.input_value = ""

def display_chat_history():
    if st.session_state.chat_history:
        with st.container():
            for i, msg in enumerate(st.session_state.chat_history):
                if msg["role"] == "user":
                    st.markdown(
                        f"<div class='user-message'><b>You:</b> {msg['content']}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='assistant-message'><b>Lumina:</b> {msg['content']}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("<hr style='border: 1px solid rgba(255, 255, 255, 0.2);'>", unsafe_allow_html=True)

# --- Sidebar Components ---
def render_sidebar():
    with st.sidebar:
        with st.container():
            st.markdown("<h2>Lumina AI ✨</h2>", unsafe_allow_html=True)
            
            # Container for Lumina info
            st.info("A cutting-edge chatbot powered by OpenRouter AI, designed to enlighten and assist. This advanced chatbot leverages the robust capabilities of OpenRouter AI, providing users with intelligent, responsive, and context-aware assistance across diverse domains. ")
            st.markdown("<h3>About me</h3>", unsafe_allow_html=True)
            
            # Container for creator info
            with st.container():
                st.info("Developed by Avinash Verma, A 4th Year Undregraduate Student from Delhi Technological University (DTU)")
                st.sidebar.markdown('<a href="https://www.linkedin.com/in/avinash-verma-584655261/"><img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG37.png" width="30" height="30" alt="Linkdln Logo"></a> [Linkdln](https://www.linkedin.com/in/avinash-verma-584655261/)',unsafe_allow_html=True)
                st.sidebar.markdown('<a href="https://leetcode.com/u/Avinash_V02/"><img src="https://leetcode.com/static/images/LeetCode_logo.png" width="30" height="30" alt="Leetcode Logo"></a> [Leetcode](https://leetcode.com/u/Avinash_V02/)',unsafe_allow_html=True)
                st.sidebar.markdown('<a href="https://www.codechef.com/users/avinash_v02"><img src="https://cutshort.io/horizontal-og-image?img=https://cdn.cutshort.io/public/companies/59a7db300adfdb705f9672e6/codechef-logo" width="30" height="30" alt="Codechef Logo"></a> [CodeChef](https://www.codechef.com/users/avinash_v02)',unsafe_allow_html=True)
                st.sidebar.markdown('<a href="https://github.com/Avinashv02"><img src="https://th.bing.com/th/id/OIP.kjCUP06WDUMR88i5wo2SqwHaHa?rs=1&pid=ImgDetMain" width="30" height="30" alt="Github Logo"></a> [Github](https://github.com/Avinashv02)',unsafe_allow_html=True)
            
            # Container for feedback section
            feedback = st.text_area("Share your thoughts (Feedback) :", key="feedback")
            if st.button("Submit Feedback"):
                if feedback.strip():
                    feedback_collection.insert_one({"feedback": feedback, "user": "anonymous", "timestamp": datetime.now()})
                    st.success("Feedback submitted!")
                    st.session_state.feedback = ""
                else:
                    st.warning("Please enter feedback.")
    return

# --- Main App ---
def main():
    themes = st.sidebar.selectbox("Choose Theme", ["Aurora", "Cosmic", "Nebula"])
    theme = render_sidebar()
    load_styles(theme, themes)
    with st.container():
        st.markdown("<h1 class='main-header'>Lumina AI ✨</h1>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
        render_chat_interface()

if __name__ == "__main__":
    main()
