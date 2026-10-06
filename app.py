import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

# Check API key
if not api_key:
    st.error("GROQ_API_KEY is missing. Please check your .env file.")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# Page settings
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a helpful, friendly, and professional AI assistant.
Your job is to answer the user's questions clearly and accurately.
Use simple language when explaining difficult topics.
If you are unsure about something, be honest and say that you are not sure.
Always remain polite and helpful."""
        }
    ]
    st.rerun()
st.write("Ask me anything!")

# Conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a helpful, friendly, and professional AI assistant.
Your job is to answer the user's questions clearly and accurately.
Use simple language when explaining difficult topics.
If you are unsure about something, be honest and say that you are not sure.
Always remain polite and helpful."""
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_message = st.chat_input("Type your message here...")

if user_message:
    
    user_message = user_message.strip()

    if not user_message:
        st.warning("Please enter a message.")
        st.stop()

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages
                )

                assistant_message = response.choices[0].message.content

                st.markdown(assistant_message)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message
                    }
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")