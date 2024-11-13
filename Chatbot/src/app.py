from dotenv import load_dotenv
import streamlit as st
from pymongo import MongoClient
import os
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

# MongoDB connection URI (replace with your actual MongoDB URI)
MONGO_URI = "mongodb+srv://avinashv02official:9891706066Avi@cluster0.yhfge.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["feedback_database"]  # Replace with your database name
feedback_collection = db["feedbacks"]  # Replace with your collection name

# Set up the Streamlit page (must be the first Streamlit command)
st.set_page_config(page_title="AI Chatbot", layout="centered", page_icon="🤖")

# Load environment variables
load_dotenv()

# Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to format text in markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Function to load OpenAI model and get response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Sidebar theme selection
theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark", "Material"])

# Custom CSS for each theme
light_theme_css = """
    <style>
    body { background-color: #FAFAFA; color: #212121; }
    .main-header { color: #6200EE; text-align: center; font-family: 'Roboto', sans-serif; }
    .stButton button { background-color: #6200EE; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #3700B3; }
    .response-text { background-color: #FFFFFF; border: 1px solid #E0E0E0; color: #424242; padding: 20px; border-radius: 8px; }
    .sidebar .sidebar-content { background-color: #F5F5F5; color: #212121; }
    .stTextInput > div > input { background-color: #FFFFFF; border: 2px solid #E0E0E0; border-radius: 8px; color: #212121; }
    </style>
"""

dark_theme_css = """
    <style>
    body { background-color: #121212; color: #E0E0E0; }
    .main-header { color: #BB86FC; text-align: center; font-family: 'Roboto', sans-serif; }
    .stButton button { background-color: #BB86FC; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #3700B3; }
    .response-text { background-color: #1E1E1E; border: 1px solid #333333; color: #E0E0E0; padding: 20px; border-radius: 8px; }
    .sidebar .sidebar-content { background-color: #333333; color: #E0E0E0; }
    .stTextInput > div > input { background-color: #333333; border: 2px solid #555555; border-radius: 8px; color: #E0E0E0; }
    </style>
"""

material_theme_css = """
    <style>
    body { background-color: #FFFFFF; color: #212121; }
    .main-header { color: #6200EE; text-align: center; font-family: 'Roboto', sans-serif; }
    .stButton button { background-color: #BB86FC; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #3700B3; }
    .response-text { background-color: #FAFAFA; border: 1px solid #E0E0E0; color: #424242; padding: 20px; border-radius: 8px; }
    .sidebar .sidebar-content { background-color: #F5F5F5; color: #212121; }
    .stTextInput > div > input { background-color: #FFFFFF; border: 2px solid #E0E0E0; border-radius: 8px; color: #212121; }
    </style>
"""

# Apply selected theme CSS
if theme == "Light":
    st.markdown(light_theme_css, unsafe_allow_html=True)
elif theme == "Dark":
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(material_theme_css, unsafe_allow_html=True)

# App title and header
st.markdown("<h1 class='main-header'>🤖 Gemini-powered AI Chatbot</h1>", unsafe_allow_html=True)
st.write("---")

# Function to handle query submission (Enter key or button click)
def handle_query():
    if st.session_state.input_query.strip():
        with st.spinner("Thinking..."):
            st.session_state.response = get_gemini_response(st.session_state.input_query)  # Store response in session state
        st.session_state.input_query = ""  # Clear the input after submission
    else:
        st.warning("Please enter a question before submitting.")


# Main chat input area, triggers `handle_query` on Enter
st.markdown("### Ask me anything!")
st.text_input("Enter your query below 👇", key="input_query", on_change=handle_query)

# Button to submit the query
if st.button("Get Response"):
    handle_query()

# Display response if available
if "response" in st.session_state and st.session_state.response:
    st.markdown("<h3 style='color: #6200EE;'>Response:</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='response-text'>{st.session_state.response}</div>", unsafe_allow_html=True)

# Sidebar with additional information and styling
st.sidebar.markdown("## About This App")
st.sidebar.info("This chatbot, powered by Gemini's generative AI, can answer a variety of questions. Simply type your query, press Enter, or click **Get Response** to see the answer.")

st.sidebar.write("---")
st.sidebar.markdown("#### Instructions")
st.sidebar.write("""
1. Enter your question in the text box.
2. Press Enter or click on **Get Response** to submit your question.
3. Wait for the AI to generate an answer.
""")
st.sidebar.info("This Chatbot is developed by Avinash Verma")
st.sidebar.info("Reach me via below")

#linkdln
st.sidebar.markdown(
    '<a href="https://www.linkedin.com/in/avinash-verma-584655261/"><img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG37.png" width="30" height="30" alt="Leetcode Logo"></a> [Linkdln](https://www.linkedin.com/in/avinash-verma-584655261/)',
    unsafe_allow_html=True
)

# leetcode
st.sidebar.markdown(
    '<a href="https://leetcode.com/u/Avinash_V02/"><img src="https://leetcode.com/static/images/LeetCode_logo.png" width="30" height="30" alt="Leetcode Logo"></a> [Leetcode](https://leetcode.com/u/Avinash_V02/)',
    unsafe_allow_html=True
)

# codechef
st.sidebar.markdown(
    '<a href="https://www.codechef.com/users/avinash_v02"><img src="https://cutshort.io/horizontal-og-image?img=https://cdn.cutshort.io/public/companies/59a7db300adfdb705f9672e6/codechef-logo" width="30" height="30" alt="Leetcode Logo"></a> [CodeChef](https://www.codechef.com/users/avinash_v02)',
    unsafe_allow_html=True
)

# Github
st.sidebar.markdown(
    '<a href="https://github.com/Avinashv02"><img src="https://th.bing.com/th/id/OIP.kjCUP06WDUMR88i5wo2SqwHaHa?rs=1&pid=ImgDetMain" width="30" height="30" alt="Leetcode Logo"></a> [Github](https://github.com/Avinashv02)',
    unsafe_allow_html=True
)

# Feedback section
st.sidebar.markdown("## Feedback")
if "feedback" not in st.session_state:
    st.session_state.feedback = ""  # Initialize session state for feedback

feedback = st.sidebar.text_area("We'd love to hear your thoughts! Please provide your feedback below:", 
                                value=st.session_state.feedback)

if st.sidebar.button("Submit Feedback"):
    if feedback.strip():
        st.sidebar.success("Thank you for your feedback!")
        
        # Save feedback to MongoDB
        feedback_document = {"feedback": feedback, "user": "anonymous"}  # You can add additional fields as needed
        feedback_collection.insert_one(feedback_document)
        
        # Clear the feedback after submission
        st.session_state.feedback = ""  # Reset the text area content
    else:
        st.sidebar.warning("Please enter your feedback before submitting.")
