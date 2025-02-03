from dotenv import load_dotenv
import streamlit as st
from pymongo import MongoClient
import os
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
from datetime import datetime
import pytz
from gtts import gTTS
import base64


# MongoDB connection URI (replace with your actual MongoDB URI)
MONGO_URI = "mongodb+srv://avinashv02official:9891706066Avi@cluster0.yhfge.mongodb.net/?retryWrites=false&tls=true"
client = MongoClient(MONGO_URI)
db = client["feedback_database"]  # Replace with your database name
feedback_collection = db["feedbacks"]  # Replace with your collection name

# Set up the Streamlit page (must be the first Streamlit command)
st.set_page_config(page_title="AI Chatbot", layout="centered", page_icon="🤖")

# Load environment variables
load_dotenv()

# Configure Google API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


# Function to format text in markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Function to load OpenAI model and get response

def get_gemini_response(question):
    model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

    #response = chat_session.send_message("INSERT_INPUT_HERE")
    response = model.generate_content(question)
    return response.text

# Sidebar theme selection
theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark", "Material"])

# Custom CSS for each theme
light_theme_css = """
    <style>
    body { background-color: #FAFAFA; color: linear-gradient(to left, #4285f4, #d96570); }
    .main-header { background: linear-gradient(to right, #5082ed, #8776d4, #b46da7, #d96570); text-align: center; font-family: 'Roboto', sans-serif; }
    .stButton button { background:  linear-gradient(to right, #5082ed, #8776d4, #b46da7, #d96570); color: white; border-radius: 8px; }
    .stButton button:hover { background:  linear-gradient(to left, #5082ed, #8776d4, #b46da7, #d96570); color: white; }
    .response-text { background-color: #FFFFFF; border: 1px solid #E0E0E0; color: #424242; padding: 20px; border-radius: 8px; }
    .sidebar .sidebar-content { background-color: #F5F5F5; color: #212121; }
    .stTextInput > div > input { background-color: #FFFFFF; border: 2px solid #E0E0E0; border-radius: 8px; color: #212121; }
    </style>
"""

dark_theme_css = """
    <style>
    body { background-color: #121212; color: #E0E0E0; }
    .main-header { color: #ed4182; text-align: center; font-family: 'Roboto', sans-serif; }
    .stButton button { background-color: #608BC1; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #133E87; color: white; }
    .response-text { background-color: #000000; border: 1px solid #333333; color: #E0E0E0; padding: 20px; border-radius: 8px; }
    .sidebar .sidebar-content { background-color: #333333; color: #E0E0E0; }
    .stTextInput > div > input { background-color: #333333; border: 2px solid #555555; border-radius: 8px; color: #E0E0E0; }
    </style>
"""

material_theme_css = """
    <style>
    body { background-color: #FFFFFF; color: #212121; }
    .main-header { color: #5BBCFF; text-align: center; font-family: 'Roboto', sans-serif; }
    .stButton button { background-color: #78B3CE; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #37AFE1; color: white; }
    .response-text { background-color: #E9EFEC; border: 1px solid #E0E0E0; color: #424242; padding: 20px; border-radius: 8px; }
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

# Function to generate and play text-to-speech audio
def play_tts(response_text):
    if response_text.strip():  # Ensure there's text to convert
        # Convert the text to speech using gTTS
        tts = gTTS(response_text, lang="en")
        audio_file = "response.mp3"
        tts.save(audio_file)
        
        # Read the audio file and encode it for Streamlit playback
        with open(audio_file, "rb") as audio:
            audio_bytes = audio.read()
            st.audio(audio_bytes, format="audio/mp3")

# Handle the user's query
def handle_query():
    """Handles user queries and responds to specific or general questions."""
    # Get and clean the user input
    question = st.session_state.input_query.strip().lower()

    # Response placeholder for showing a response or spinner
    response_placeholder = st.empty()
    b = 0

    # Check for specific types of queries
    developer_related_phrases = ["who are you", "who developed you", "who created you", "who made you"]
    time_related_phrases = ["what time", "current time", "tell me the time", "what is the time", "time right now", "time"]
    greed_related_phrases = ["how are you"]
    
    if any(phrase in question for phrase in developer_related_phrases):
        b = 1
        # Predefined response for developer-related queries
        st.session_state.response = (
            "Hello, I am <span style='font-family: Parkinsans, sans-serif; font-weight: bold;'>Lumina</span> "
            "(light and intelligence), an AI chatbot.<br><hr>"
            "Powered by gemini which is developed using a large language model, developed and trained by Google."
            " This is a project work by Avinash Verma, from Delhi Technological University(DTU)."
            " You can reach him using linkdln👉"
            '<a href="https://www.linkedin.com/in/avinash-verma-584655261/"><img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG37.png" width="30" height="30" alt=""></a>'
        )
    elif any(phrase in question for phrase in time_related_phrases):
        b = 1
        # Get the current time in 12-hour format
        current_time = datetime.now().strftime("%I:%M:%S %p")
        st.session_state.response = f"The current time is: {current_time} (UTC)"
    elif any(phrase in question for phrase in greed_related_phrases):
        b = 1
        st.session_state.response = "I'm just a bundle of code, so I don't have feelings, but thanks for asking! How can I assist you today? 😊"
    elif question:
        b = 1
        # Display a spinner while processing the query
        with st.spinner("Thinking..."):
            # Call the AI response function and set the response
            st.session_state.response = get_gemini_response(question)
    else:
        b = 0
        # Warning for empty input
        st.warning("Please enter a question before submitting.")
        response_placeholder.empty()

    # if b == 1:
    #     # Display the response
    #     response_placeholder.markdown(f"**Response:** {st.session_state.response}")
    #     # Clear the input field after submission
    #     st.session_state.input_query = ""



# Main chat input area, triggers `handle_query` on Enter
st.markdown("### Ask me anything!")
st.text_input("Enter your query below 👇", key="input_query", on_change=handle_query)

# Button to submit the query
if st.button("Get Response"):
    handle_query()

# Display response if available and add TTS playback
if "response" in st.session_state and st.session_state.response:
    st.markdown("<h3 style='color: #6200EE;'>Response:</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='response-text'>{st.session_state.response}</div>", unsafe_allow_html=True)
    
    # Play the response text as audio
    play_tts(st.session_state.response)
    
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
    '<a href="https://www.linkedin.com/in/avinash-verma-584655261/"><img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG37.png" width="30" height="30" alt="Linkdln Logo"></a> [Linkdln](https://www.linkedin.com/in/avinash-verma-584655261/)',
    unsafe_allow_html=True
)

# leetcode
st.sidebar.markdown(
    '<a href="https://leetcode.com/u/Avinash_V02/"><img src="https://leetcode.com/static/images/LeetCode_logo.png" width="30" height="30" alt="Leetcode Logo"></a> [Leetcode](https://leetcode.com/u/Avinash_V02/)',
    unsafe_allow_html=True
)

# codechef
st.sidebar.markdown(
    '<a href="https://www.codechef.com/users/avinash_v02"><img src="https://cutshort.io/horizontal-og-image?img=https://cdn.cutshort.io/public/companies/59a7db300adfdb705f9672e6/codechef-logo" width="30" height="30" alt="Codechef Logo"></a> [CodeChef](https://www.codechef.com/users/avinash_v02)',
    unsafe_allow_html=True
)

# Github
st.sidebar.markdown(
    '<a href="https://github.com/Avinashv02"><img src="https://th.bing.com/th/id/OIP.kjCUP06WDUMR88i5wo2SqwHaHa?rs=1&pid=ImgDetMain" width="30" height="30" alt="Github Logo"></a> [Github](https://github.com/Avinashv02)',
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
