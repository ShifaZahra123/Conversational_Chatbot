import streamlit as st
import google.generativeai as genai
from google.generativeai.types import StopCandidateException

# Retrieve the API key from Streamlit secrets
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

# Instantiate the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Define chatbot behavior
chatbot_instructions = """Your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. 
Please provide accurate and helpful information, and always maintain a polite and professional tone.

1. Greet the user politely, ask for their name, and ask how you can assist them with AI-related queries.
2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learning, natural language processing, computer vision, and related topics.
3. Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
5. Be patient and considerate when responding to user queries, and provide clear explanations.
6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
7. Do not generate long paragraphs in response. Maximum words should be 100.

Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being."""

def ai_chatbot(prompt):
    chat_session = model.start_chat(
        history=[
            {
                "role": "system",
                "parts": [chatbot_instructions],  # Provide instructions to the chatbot
            },
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
st.title("AI Mentor")

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
            st.markdown(f"<div style='text-align: left;'>🤖 {message['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: right;'>{message['message']} 😎</div>", unsafe_allow_html=True)

# End conversation button
if st.button("End Conversation"):
    st.write("AI Mentor: Goodbye! It was nice talking to you.")
    st.session_state['history'] = []  # Clear history
