import requests
import base64
import mimetypes
import os
from urllib.parse import urlparse
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults, WikipediaQueryRun
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.document_loaders import WikipediaLoader


from openai import OpenAI
from typing import List, Dict, Any

import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.environ.get("OPENAI_API_KEY")
tavily_api_key = os.environ.get("tavily_api_key")



@tool
def get_youtube_trancript(video_url: str) -> str:
    """Fetches transcript of the youtube video at the given URL.
    Args:
        video_url (str): The URL of the YouTube video.
    """

    try:
        video_id = video_url.split("v=")[-1]
        ytt_api = YouTubeTranscriptApi()
        # We could add the option to load the transcript in a specific language
        transcript = ytt_api.fetch(video_id)
        sentences = []
        for t in transcript:
            start = t.start
            end = start + t.duration
            sentences.append(f"{start:.2f} - {end:.2f}: {t.text}")
        transcript_with_timestamps = "\n".join(sentences)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        transcript_with_timestamps = ""


    if not transcript_with_timestamps:
        return "Could not fetch transcript."

    # Use fallbacks for whichever is missing

    transcript_section = (
        f"\n\nTranscript:\n{transcript_with_timestamps}"
        if transcript_with_timestamps
        else "\n\nTranscript not available."
    )
    return f"{transcript_section}"

@tool
def web_search(query: str) -> str:
    """Search Tavily for a query and return at most 3 results."""
    tavily = TavilySearchResults(
        max_results=3,
        include_answer=True,       # optional; see docs
        include_raw_content=True,  # optional; see docs
    )

    # Per docs, invoke takes a str | dict | ToolCall as `input`
    results: List[Dict[str, Any]] = tavily.invoke(query)

    # Results are JSON-like dicts, not langchain.schema.Document objects.
    # Typical keys: 'url', 'content', 'score', 'title', etc. (may vary with params)
    formatted = "\n\n---\n\n".join(
        f'<Document source="{r.get("url", "")}" score="{r.get("score", "")}">\n'
        f'{r.get("content", r)}\n'
        f'</Document>'
        for r in results
    )
    return formatted


@tool
def wiki_search(query: str) -> str:
    """Search Wikipedia for a query and return maximum 2 results.
    Args:
        query: The search query."""
    search_docs = WikipediaLoader(query=query, load_max_docs=2).load()
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"wiki_results": formatted_search_docs} 

wikipedia_api = WikipediaAPIWrapper(top_k_results=2)

@tool
def image_input_response(query: str, image_path: str) -> str:
    """    
    Sends a query with an image_path to the OpenAI API and returns the response.
    Args:
        query (str): The query to send.
        image_path (str): The filepath of the image to include in the request.
    Returns:
        str: The response from the OpenAI API.
    """
    client = OpenAI( 
        api_key=openai_key
    )

    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None or not mime_type.startswith('image/'):
            # Default to common image types or detect from file extension
            file_ext = image_path.lower().split('.')[-1]
            mime_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp',
                'bmp': 'image/bmp'
            }
            mime_type = mime_type_map.get(file_ext, 'image/jpeg')

        # Create the data URL format
        image_url = f"data:{mime_type};base64,{base64_image}"

        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": query},
                        {
                            "type": "input_image",
                            "image_url": image_url
                        }
                    ]
                }
            ]
        )
        return response.output_text
    except Exception as e:
        return f"Error fetching response: {e}. Try file input instead."
    
@tool
def file_input_response(query: str, file_path: str) -> str:
    """    
    Sends a query with a file path to a PDF File to the OpenAI API and returns the response.
    Args:
        query (str): The query to send.
        file_path (str): The filepath of the PDF file to include in the request.
    Returns:
        str: The response from the OpenAI API.
    """
    client = OpenAI( 
        api_key=openai_key
    )

    try:
    # Read and encode the PDF file as base64
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')

        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": query},
                        {
                            "type": "input_file",
                            "filename": "temp.pdf",
                            "file_data": f"data:application/pdf;base64,{base64_pdf}"
                        }
                    ]
                }
            ]
        )
        return response.output_text
    except Exception as e:
        return f"Error fetching response: {e}. Try image input instead."

@tool
def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio from a audio file using OpenAI's Whisper model.
    Args:
        file_path (str): Path to the audio file.
    Returns:
        str: Transcription of the audio.
    """
    client = OpenAI(api_key=openai_key)
    file = open(file_path, "rb")

    try:
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=file,
            response_format="text"
        )
        return response
    except Exception as e:
        return f"Error transcribing audio: {e}"

@tool
def download_question_file(url: str, save_dir: str = ".") -> str:
    """
    Downloads the file associated with a given URL
    Args:
        url (str): id to download the file
        save_dir (str): Directory to save the downloaded file.
    Returns:
        str: Path to the saved file, or an error message.
    """

    
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        
        # Determine file extension from URL or content type
        parsed_url = urlparse(url)
        url_filename = os.path.basename(parsed_url.path)
        
        if url_filename and '.' in url_filename:
            # Use filename from URL if it has an extension
            filename = url_filename
        else:
            # Determine extension from content type
            content_type = resp.headers.get('content-type', '').lower()
            
            if 'json' in content_type:
                filename = "temp.json"
            elif 'text/plain' in content_type or 'text/' in content_type:
                filename = "temp.txt"
            elif 'application/pdf' in content_type:
                filename = "temp.pdf"
            elif 'image/png' in content_type:
                filename = "temp.png"
            elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
                filename = "temp.jpg"
            elif 'text/html' in content_type:
                filename = "temp.html"
            elif 'application/xml' in content_type or 'text/xml' in content_type:
                filename = "temp.xml"
            elif 'text/csv' in content_type:
                filename = "temp.csv"
            else:
                # Try to guess from content or default to .txt
                content_preview = resp.content[:100].decode('utf-8', errors='ignore').strip()
                if content_preview.startswith('{') or content_preview.startswith('['):
                    filename = "temp.json"
                elif content_preview.startswith('<'):
                    filename = "temp.html"
                else:
                    filename = "temp.txt"
    
    except requests.exceptions.HTTPError as e:
        return f"HTTP error: {e.response.status_code}"
    except Exception as e:
        return f"Network error: {e}"
    
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)
    
    # Write file (will overwrite if it exists)
    with open(file_path, "wb") as f:
        f.write(resp.content)
    
    return file_path

def build_agent():
    llm = ChatOpenAI(
    model="gpt-4.1",
    api_key = openai_key)

    tools=[
        web_search,
        WikipediaQueryRun(api_wrapper=wikipedia_api),
        wiki_search,
        get_youtube_trancript,
        image_input_response,
        file_input_response,
        download_question_file,
        transcribe_audio
    ]
    llm_with_tools = llm.bind_tools(
        tools=tools
    )

    class AgentState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]

    def assistant(state: AgentState):
        return {
            "messages": [llm_with_tools.invoke(state["messages"])],
        }


    builder = StateGraph(AgentState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    return builder.compile()

