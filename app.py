import streamlit as st
import os
import tempfile
from agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage
import base64
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="General AI Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            file_path = tmp_file.name
            file_path_message = f"File uploaded in path: {file_path}"
            human_message = HumanMessage(content=file_path_message)
            st.session_state.messages.append(human_message)
            return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("General AI Assistant")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        tavily_key = st.text_input("Tavily API Key", type="password", help="Enter your Tavily API key")
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        if tavily_key:
            os.environ["tavily_api_key"] = tavily_key
        
        # Initialize agent button
        if st.button("Initialize Agent", type="primary"):
            if not api_key:
                st.error("Please enter your OpenAI API key first!")
            else:
                with st.spinner("Initializing GAIA agent..."):
                    try:
                        st.session_state.agent = build_agent()
                        st.success("Agent initialized successfully!")
                    except Exception as e:
                        st.error(f"Error initializing agent: {e}")
        
        # File upload section
        st.header("File Upload")
        
        uploaded_files = st.file_uploader(
            "Upload files (images, PDFs, audio, etc.)",
            type=['png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp3', 'wav', 'm4a', 'txt', 'json', 'csv'],
            help="Upload multiple files to analyze with GAIA",
            accept_multiple_files=True
        )
        
        # Process uploaded files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Only process if file is not already in session state
                if uploaded_file.name not in st.session_state.uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    if file_path:
                        st.session_state.uploaded_files[uploaded_file.name] = file_path
                        st.success(f"{uploaded_file.name} uploaded successfully!")
            

    # Main chat area
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Chat messages container
        chat_container = st.container(height=600)
        
        with chat_container:
            # Display chat messages
            for message in st.session_state.messages:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)
        
        # Chat input
        user_input = st.chat_input("Ask GAIA anything...")
        
        if user_input:
            if not st.session_state.agent:
                st.error("Please initialize the agent first!")
            else:
                # Add user message to chat
                human_message = HumanMessage(content=user_input)
                st.session_state.messages.append(human_message)
                
                # Get agent response
                with st.spinner("GAIA is thinking..."):
                    try:
                        result = st.session_state.agent.invoke({"messages": st.session_state.messages})
                        ai_message = result["messages"][-1]
                        st.session_state.messages.append(ai_message)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error getting response: {e}")
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        st.header("Available Tools")
        tools_info = [
            "Web Search",
            "Wikipedia Search", 
            "YouTube Transcripts",
            "Image Analysis",
            "PDF Analysis",
            "Audio Transcription",
            "File Download"
        ]
        
        for tool in tools_info:
            st.write(f"• {tool}")
        
        # Agent status
        st.header("Agent Status")
        if st.session_state.agent:
            st.success("Agent Ready")
        else:
            st.warning("Agent Not Initialized")
        

if __name__ == "__main__":
    main()