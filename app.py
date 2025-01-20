# -*- coding: utf-8 -*-
!pip install streamlit pyngrok

import os
import google.generativeai as genai
import streamlit as st
from pyngrok import ngrok

# Set up the API key
os.environ['API_KEY'] = "API Key"
genai.configure(api_key=os.environ['API_KEY'])

# Load the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to interact with the job preparation chatbot
def generate_job_preparation_response(user_input):
    prompt = f"""
    You are a job preparation assistant. You assist users with answering interview questions, provide tips for aptitude tests, and group discussions.
    - Respond only to questions related to job interviews, aptitude tests, and professional career development.
    - If the user asks anything unrelated to job preparation, politely inform them that you can only provide job preparation advice.
    - Provide accurate, concise, and professional responses.
    - Always respond in a friendly and supportive tone.

    User's question: {user_input}
    """

    # Generate response based on job preparation prompt
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        generation_config={"temperature": 0.7}  # Control creativity
    )

    assistant_reply = response.candidates[0].content
    return assistant_reply

# Streamlit UI inside a container
st.markdown("""
    <style>
    .chatbox-container {
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 20px;
        background-color: #ffffff;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        height: 500px;
        position: relative;
    }
    .chat-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        overflow-y: auto;
        flex-grow: 1;
        display: flex;
        flex-direction: column-reverse;
        margin-bottom: 60px;
    }
    .user-bubble {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color: #e0e0e0;
        color: black;
        padding: 12px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    .clear {
        clear: both;
    }
    .stTextInput>div {
        position: relative;
        width: 100%;
    }
    .stTextInput>div>input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        width: 92%;
        left: 4%;
        padding-right: 40px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        border-radius: 10px;
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        font-weight: bold;
        border: none;
        background-image: url('https://www.google.com/imgres?q=submit%20button%20icon%20img&imgurl=http%3A%2F%2Fwww.clker.com%2Fcliparts%2F8%2FX%2Fy%2F7%2FJ%2Fp%2Fsubmit-button.svg.hi.png&imgrefurl=http%3A%2F%2Fwww.clker.com%2Fclipart-submit-button-7.html&docid=RtqN3_kO4urR4M&tbnid=lGBXVqGi4lOBxM&vet=12ahUKEwim_8m9pIKLAxVDd2wGHZGrNSsQM3oECEUQAA..i&w=600&h=300&hcb=2&ved=2ahUKEwim_8m9pIKLAxVDd2wGHZGrNSsQM3oECEUQAA');
        background-size: 30px;
        background-repeat: no-repeat;
        background-position: center;
        cursor: pointer;
    }
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .title-container img {
        width: 80px;
        height: 80px;
        margin-right: 0;
        border-radius: 50%;
        object-fit: cover;
    }
    .stTextInput {
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing messages if it does not exist
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Create a form inside the container to make everything align together
with st.form(key="job_preparation_form", clear_on_submit=True):
    st.markdown("""
        <div class="title-container">
            <h1>Job Preparation Chatbot</h1>
            <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxIREhUSExIWFhUXFhUXGBgYGBUWGBgZFxYXGhkXGxcYHSggGBslGxcWITEhJSkrLi4uFx8zODMsNygtLisBCgoKDg0OGxAQGy4mICYtLS0rLS0t
    </style>
    """)

    st.write("Ask me anything about job preparation, aptitude tests, and interview tips!")

    # Display chat history and handle input/output above the input box
    with st.container():
        for message in reversed(st.session_state['messages']):
            if message['role'] == "user":
                st.markdown(f"<div class='user-bubble'>{message['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-bubble'>{message['text']}</div>", unsafe_allow_html=True)

        st.markdown('<div class="clear"></div>', unsafe_allow_html=True)

    # Take user input and submit button
    user_input = st.text_input("You:")

    # Submit button
    submit_button = st.form_submit_button(label="Submit")

    # Handle user input and generate response
    if user_input and submit_button:
        # Add user message to session state
        st.session_state['messages'].append({"role": "user", "text": user_input})

        # Generate response based on user input
        response = generate_job_preparation_response(user_input)

        # Add bot response to session state
        st.session_state['messages'].append({"role": "bot", "text": response})

# Add your ngrok authtoken to authenticate your account
!ngrok authtoken <Add token>

# Set up ngrok tunnel for Streamlit
public_url = ngrok.connect(8501)
print(f"Streamlit app is live at: {public_url}")

!streamlit run app.py
