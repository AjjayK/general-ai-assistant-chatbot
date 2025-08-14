# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
GAIA Chatbot is an AI agent built with LangGraph and Streamlit that combines multiple AI tools for web search, file analysis, transcription, and multimodal interactions. The system uses GPT-4 as the core reasoning model with integrated tools for various tasks.

## Core Architecture

### Agent System (agent.py)
- **LangGraph-based agent** with StateGraph workflow management
- **Core LLM**: ChatOpenAI with GPT-4.1 model
- **Tool Integration**: Uses LangChain's tool binding system with ToolNode
- **State Management**: TypedDict-based AgentState with message accumulation
- **Conditional Routing**: Uses tools_condition for dynamic tool selection

### Available Tools
The agent has access to these integrated tools:
- `web_search`: Tavily API integration for internet search (max 3 results)
- `wiki_search`: Wikipedia content retrieval (max 2 documents)
- `get_youtube_trancript`: YouTube video transcript extraction
- `image_input_response`: GPT-4 Vision analysis for images
- `file_input_response`: PDF document analysis
- `transcribe_audio`: Whisper-based audio transcription
- `download_question_file`: URL-based file downloading with smart type detection

### Streamlit Interface (app.py)
- **Session Management**: Persistent chat history and file uploads
- **File Handling**: Temporary file management with automatic cleanup
- **Multi-modal Support**: Image preview, PDF indicators, audio file handling
- **Responsive Layout**: Sidebar configuration, main chat area, tools panel

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (Windows)
gaia_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start Streamlit app
streamlit run app.py
```

### Environment Configuration
Create a `.env` file with required API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
tavily_api_key=your_tavily_api_key_here
```

## Code Architecture Patterns

### Tool Function Structure
All tools follow this pattern:
- `@tool` decorator for LangChain integration
- Type hints for parameters and return values
- Comprehensive error handling with fallback responses
- Structured return formats (often with metadata)

### Agent Workflow
1. User input processed through HumanMessage
2. LLM with bound tools determines action
3. Conditional routing to either tools or direct response
4. Tool results fed back to assistant for final response
5. State accumulates all messages for context

### File Processing Strategy
- Smart MIME type detection for uploads
- Base64 encoding for API transmission
- Temporary file management with cleanup
- Support for images, PDFs, audio, and text formats

## Key Implementation Notes

### OpenAI API Usage
- Uses custom `client.responses.create()` calls for vision/file tasks
- Model specification: "gpt-4.1" for chat, "gpt-4o-transcribe" for audio
- Structured input format with role-based content arrays

### Error Handling
- All tools include comprehensive try/catch blocks
- Fallback suggestions when primary methods fail
- User-friendly error messages for common issues

### State Management
- Streamlit session_state for persistence
- Message history maintains conversation context
- File upload state tracking with cleanup capabilities