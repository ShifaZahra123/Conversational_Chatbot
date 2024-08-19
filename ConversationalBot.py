import streamlit as st
import google.generativeai as genai
from google.generativeai.types import StopCandidateException
import os

# Retrieve the API key from Streamlit secrets
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 0.7,  # Controls the randomness of the response
    "top_p": 0.9,        # Controls the diversity of the response
    "top_k": 50,         # Limits the sampling pool to the top k choices
    "max_output_tokens": 500,  # Maximum length of the response
    "response_mime_type": "text/plain",
}

# Instantiate the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def ai_chatbot(prompt):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            }
        ]
    )
    try:
        response = chat_session.send_message(prompt)
        return response.text.strip()
    except StopCandidateException as e:
        # Handle the StopCandidateException
        return "I'm sorry, I seem to be repeating myself. Could you try rephrasing your question?" 

# Streamlit app interface
st.title("AI Chatbot")

# Display the "End Conversation" button at the top
if st.button("End Conversation"):
    st.write("Chatbot: Goodbye! It was nice talking to you.")
    st.stop()  # Stop further processing to end the conversation

# Display the chat history
if 'history' not in st.session_state:
    st.session_state.history = []

for entry in reversed(st.session_state.history):
    st.write(f"{entry['role'].capitalize()}: {entry['parts'][0]}")

# User input
user_input = st.text_input("You: ", "")

if user_input:
    response = ai_chatbot(user_input)
    st.session_state.history.append({"role": "user", "parts": [user_input]})
    st.session_state.history.append({"role": "chatbot", "parts": [response]})
    st.write(f"Chatbot: {response}")
    st.text_input("You: ", "", key="input")  # Clear the input field
