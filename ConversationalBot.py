import streamlit as st
import google.generativeai as genai
from google.generativeai.types import StopCandidateException

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
    except StopCandidateException:
        # Handle the StopCandidateException
        return "I'm sorry, I seem to be repeating myself. Could you try rephrasing your question?"

# Streamlit app interface
st.title("AI Chatbot")

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state['history'] = []  # Store chat history

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""  # Store current user input

# Handle user input
def handle_input():
    if st.session_state.user_input:
        response = ai_chatbot(st.session_state.user_input)
        st.session_state.history.append({
            "role": "user",
            "message": st.session_state.user_input
        })
        st.session_state.history.append({
            "role": "ai",
            "message": response
        })
        st.session_state.user_input = ""  # Clear input field after submission

# User input
st.text_input("You: ", key='user_input', on_change=handle_input)

# Display chat history
if st.session_state['history']:
    for message in reversed(st.session_state['history']):
        if message["role"] == "ai":
            st.write(f"Chatbot: {message['message']}")
        else:
            st.write(f"You: {message['message']}")

# End conversation button
if st.button("End Conversation"):
    st.write("Chatbot: Goodbye! It was nice talking to you.")
    st.session_state['history'] = []  # Clear history
