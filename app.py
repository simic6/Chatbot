
import requests
import streamlit as st

# Configure the page
st.set_page_config(
    page_title="My Free AI Chatbot",
    page_icon="🤖",
)

st.title("🤖 My Free AI Chatbot")
st.caption("Powered by Python and Ollama — runs locally")

MODEL = "llama3.2:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.write(f"AI model: {MODEL}")
    st.write("No OpenAI API key required.")

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get a new message
prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "messages": st.session_state.messages,
                        "stream": False,
                    },
                    timeout=300,
                )

                response.raise_for_status()
                answer = response.json()["message"]["content"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                })

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to Ollama. "
                    "Make sure Ollama is installed and running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The AI took too long to respond. "
                    "Try again or use a smaller model."
                )

            except requests.exceptions.RequestException as error:
                st.error(f"Ollama request failed: {error}")

            except (KeyError, ValueError):
                st.error("Could not read the AI response.")
