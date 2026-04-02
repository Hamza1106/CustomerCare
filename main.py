import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("keys.env")

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# System prompt for e-commerce customer support
SYSTEM_PROMPT = """You are a helpful customer support assistant for "TechStore" - an online electronics store.

Your responsibilities:
- Answer product questions (laptops, phones, accessories)
- Help with order status and tracking
- Explain return and refund policies
- Provide shipping information
- Handle complaints professionally

Store Policies:
- Free shipping on orders above $50
- 30-day return policy
- 24/7 customer support
- 2-year warranty on electronics

Be friendly, professional, and concise. If you don't know something, offer to connect them with a human agent.
"""

# Page config
st.set_page_config(
    page_title="TechStore Support Bot",
    page_icon="🛒",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stChatMessage {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🛒 TechStore Support Bot")
st.caption("Ask me anything about products, orders, or policies!")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={
            'temperature': 0.7,
            'max_output_tokens': 500,
        }
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])
    
    # Send system prompt (hidden from user)
    st.session_state.chat.send_message(SYSTEM_PROMPT)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to history
    st.session_state.messages.append({
        'role': 'user',
        'content': prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                bot_reply = response.text
                
                st.write(bot_reply)
                
                # Add to history
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': bot_reply
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This chatbot can help you with:
    - Product inquiries
    - Order tracking
    - Return & refund policies
    - Shipping information
    - General support
    """)
    
    st.divider()
    
    # Quick actions
    st.subheader("Quick Questions")
    if st.button("📦 Track my order"):
        st.session_state.messages.append({
            'role': 'user',
            'content': 'How can I track my order?'
        })
        st.rerun()
    
    if st.button("🔄 Return policy"):
        st.session_state.messages.append({
            'role': 'user',
            'content': 'What is your return policy?'
        })
        st.rerun()
    
    if st.button("🚚 Shipping info"):
        st.session_state.messages.append({
            'role': 'user',
            'content': 'Tell me about shipping options'
        })
        st.rerun()
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = st.session_state.model.start_chat(history=[])
        st.session_state.chat.send_message(SYSTEM_PROMPT)
        st.rerun()
    
    st.divider()
    st.caption("Built by Hamza Akhtar")
    st.caption("Powered by Google Gemini")