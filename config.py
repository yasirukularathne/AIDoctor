import os
from dotenv import load_dotenv

# Create temp directory path - this is a constant
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")

def setup_environment():
    """Initialize environment settings and directories"""
    # Load environment variables
    load_dotenv()
    
    # Create temp directory if needed
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Check API key and warn if missing
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("⚠️ WARNING: GROQ_API_KEY not found in environment!")
        print("Create a .env file with your GROQ_API_KEY=your_key_here")
    
    return TEMP_DIR, api_key