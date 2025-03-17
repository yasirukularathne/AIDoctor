import os
from dotenv import load_dotenv
import base64
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import mimetypes

# Load environment variables
load_dotenv()

def get_image_mime_type(image_path):
    """Get the MIME type of an image file"""
    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type or 'image/jpeg'  # Default to jpeg if unable to determine

def encode_image(image_path):
    """Encode an image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            mime_type = get_image_mime_type(image_path)
            return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def query_text_model(query, model="mixtral-8x7b-32768", temperature=0.7):
    """Send a text-only query to the LLM model"""
    try:
        # Get API key
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        # Initialize client
        client = Groq(api_key=api_key)
        
        # Text-only chat completion
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful medical professional."},
                {"role": "user", "content": query}
            ],
            model=model,
            temperature=temperature,
            max_tokens=1024
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error querying text model: {str(e)}")
        raise e

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def analyze_image_with_query(query, encoded_image, model="mixtral-8x7b-32768"):
    """
    Text-only analysis that works with Groq models.
    Note: This doesn't actually analyze the image as Groq doesn't support images,
    but creates a response based on the text query only.
    """
    try:
        # Create an image-aware prompt even though we can't process the image
        if encoded_image:
            print("Note: Image provided, but using text-only analysis as Groq doesn't support image input")
            enhanced_query = f"""
            {query}
            
            [Note: The user has also shared a medical image that I cannot directly view.
            I'll provide general guidance based on their text description.]
            """
        else:
            enhanced_query = query
        
        # Use the text-only model
        return query_text_model(enhanced_query, model=model)
    
    except Exception as e:
        print(f"Error in analyze_image_with_query: {str(e)}")
        raise e

# Define available vision models
VISION_MODELS = [
    "llama-3.2-90b-vision-preview",  # Most capable vision model
    "llama-3.2-70b-vision-preview",  # Good balance of performance and speed
    "llama-3.2-35b-vision-preview",  # Faster, still decent quality
    "llama-3.2-11b-vision-preview",  # Fastest, but less capable
]

# Update the model selection in your code
def try_vision_models(client, messages):
    preferred_model = "llama-3.2-90b-vision-preview"  # Most capable model
    fallback_models = [
        "llama-3.2-70b-vision-preview",
        "llama-3.2-35b-vision-preview",
        "llama-3.2-11b-vision-preview"
    ]
    
    models_to_try = [preferred_model] + fallback_models
    
    for model in models_to_try:
        try:
            print(f"\nTrying model: {model}")
            response = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.5,  # Lower temperature for more precise answers
                max_tokens=1000   # Increase tokens for detailed responses
            )
            content = response.choices[0].message.content
            # Basic response validation
            if content and len(content) > 20:  # Arbitrary threshold for meaningful response
                print(f"Success with model: {model}")
                return response
            else:
                print(f"Model {model} returned insufficient response: {content}")
        except Exception as e:
            print(f"Model {model} failed: {str(e)}")
            continue
    raise Exception("All models failed or returned insufficient responses")

# Main execution
try:
    # Load environment variables
    load_dotenv()
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
    # Initialize client with API key
    client = Groq(api_key=GROQ_API_KEY)
    
    # Image path and encoding
    image_path = "images.jpg"
    print(f"Processing image: {image_path}")
    image_url = encode_image(image_path)
    print("Image successfully encoded")
    
    # Setup query parameters
    query = "Is there something wrong with this image?"
    
    # Prepare messages with proper image format
    messages = [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "high"  # Request high detail analysis
                }
            }
        ]
    }]
    
    print("Attempting to use available vision models...")
    response = try_vision_models(client, messages)
    
    print("\nResponse from model:")
    print(response.choices[0].message.content)

except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found")
except Exception as e:
    print(f"Error: {str(e)}")
    if hasattr(e, 'response'):
        print(f"Response details: {e.response.text if hasattr(e.response, 'text') else e.response}")