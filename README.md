# GAIA Chatbot 🤖

A powerful AI chatbot built with LangGraph and Streamlit that can search the web, analyze files, transcribe audio, and more!

## Features

- 🔍 **Web Search**: Search the internet for current information
- 📚 **Wikipedia Integration**: Access Wikipedia articles
- 📺 **YouTube Transcripts**: Get transcripts from YouTube videos
- 🖼️ **Image Analysis**: Analyze images using GPT-4 Vision
- 📄 **PDF Analysis**: Extract and analyze content from PDF files
- 🎵 **Audio Transcription**: Transcribe audio files using Whisper
- 📥 **File Download**: Download and analyze files from URLs
- 💬 **Chat Interface**: Beautiful Streamlit-based chat interface

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. API Keys Setup

You have two options for providing API keys:

#### Option 1: Streamlit Interface (Recommended)
- Enter your API keys directly in the Streamlit sidebar when you run the app
- More secure as keys are not stored in files

#### Option 2: Environment File (Optional)
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
tavily_api_key=your_tavily_api_key_here
```

**Required API Keys:**
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys) - Required
- **Tavily API Key**: Get from [Tavily](https://tavily.com/) - Optional, for web search

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### 1. Initialize the Agent
1. Open the Streamlit app
2. Enter your API keys in the sidebar (or use .env file)
3. Click "Initialize Agent"

### 2. Start Chatting
- Type your questions in the chat area
- The agent will use its tools to find answers
- Upload files to analyze them

### 3. File Upload
Supported file types:
- **Images**: PNG, JPG, JPEG, GIF
- **Documents**: PDF, TXT, JSON, CSV
- **Audio**: MP3, WAV, M4A

### 4. Example Queries

```
"Search for the latest news about AI"
"Get the transcript of this YouTube video: https://youtube.com/watch?v=..."
"Analyze this image and describe what you see"
"Summarize this PDF document"
"Transcribe this audio file"
"What is machine learning according to Wikipedia?"
```

## Available Tools

| Tool | Description |
|------|-------------|
| 🔍 Web Search | Search the internet using Tavily |
| 📚 Wikipedia Search | Search and retrieve Wikipedia articles |
| 📺 YouTube Transcripts | Get transcripts from YouTube videos |
| 🖼️ Image Analysis | Analyze images using GPT-4 Vision |
| 📄 PDF Analysis | Extract and analyze PDF content |
| 🎵 Audio Transcription | Transcribe audio using Whisper |
| 📥 File Download | Download files from URLs |

## Project Structure

```
GAIA-Chatbot/
├── agent.py          # Main agent implementation
├── app.py           # Streamlit web interface
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (optional)
├── .gitignore       # Git ignore file
└── README.md        # This file
```

## Technical Details

### Agent Architecture
- Built with **LangGraph** for workflow management
- Uses **LangChain** for tool integration
- Powered by **GPT-4** for reasoning and responses

### Tools Integration
- **Tavily Search**: Web search capabilities
- **Wikipedia API**: Knowledge base access
- **YouTube Transcript API**: Video transcript extraction
- **OpenAI API**: Image analysis, PDF processing, audio transcription

### Streamlit Features
- Real-time chat interface
- File upload and management
- Session state management
- Responsive design
- Export chat functionality

## Troubleshooting

### Common Issues

1. **Agent not initializing**
   - Check your API keys are correct
   - Ensure you have sufficient OpenAI credits
   - Verify internet connection

2. **File upload errors**
   - Check file size limits
   - Ensure file format is supported
   - Verify file is not corrupted

3. **Tool errors**
   - Check API rate limits
   - Verify API keys are valid
   - Ensure required services are available

### Error Messages

- `"Please enter your OpenAI API key first!"` - Add your API key in the sidebar
- `"Error initializing agent"` - Check API keys and internet connection
- `"Error getting response"` - Check OpenAI API status and credits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the app
3. Ensure all dependencies are installed correctly
4. Verify your API keys are valid and have sufficient credits

---

**Happy chatting with GAIA! 🤖✨** 