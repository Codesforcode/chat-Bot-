import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Mistral AI Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize model (cached)
@st.cache_resource
def load_model():
    return ChatMistralAI(model="mistral-small-latest")

model = load_model()

# Header
st.title("🤖 Mistral AI Chat")

# Display chat messages using st.chat_message (super fast!)
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:  # AIMessage
        with st.chat_message("assistant"):
            st.write(message.content)

# Input handling with chat_input (fast & optimized)
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Display user message immediately
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.invoke(st.session_state.messages)
            st.write(response.content)
    
    # Add AI message to history
    st.session_state.messages.append(AIMessage(content=response.content))

# Sidebar options
with st.sidebar:
    st.title("⚙️ Options")
    
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Made with **Mistral AI** ✨")