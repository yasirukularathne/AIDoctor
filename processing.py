import os
from config import TEMP_DIR
from prompts import INITIAL_PROMPT, FOLLOWUP_PROMPT
from DoctorsBrain import encode_image, analyze_image_with_query, query_text_model
from VoicePatient import transcribe_with_groq
from VoiceDoctor import text_to_speech_with_gtts

# Record of previous conversation for context
conversation_history = []

def format_conversation_context(history):
    """Format conversation history into readable context"""
    if not history:
        return ""
        
    context = "\n\nPrevious conversation:\n"
    for entry in history:
        context += f"{entry[0]}: {entry[1]}\n"
    return context

def process_initial_consultation(audio_filepath, image_filepath):
    """Process the initial consultation with audio and image inputs"""
    global conversation_history
    
    try:
        # Ensure we have valid input
        if not audio_filepath:
            return "No audio provided", "Please record your symptoms first", None, []
            
        # Get API key - fail early if missing
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "API key error", "Please set a valid GROQ_API_KEY in your .env file", None, []
            
        # Transcribe audio
        print(f"Processing audio: {audio_filepath}")
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=api_key, 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        print(f"Transcription: {speech_to_text_output}")

        # Create a medical prompt with the patient's symptoms
        medical_prompt = f"""
        As a doctor, I'm reviewing a patient who says: "{speech_to_text_output}"
        
        Based on this description, I should:
        1. Consider possible conditions that match these symptoms
        2. Provide a professional assessment
        3. Recommend appropriate next steps
        
        My assessment:
        """

        # Get doctor's response
        doctor_response = query_text_model(
            query=medical_prompt,
            model="mixtral-8x7b-32768"
        )

        # Generate audio response
        print("Generating voice response")
        output_filepath = os.path.join(TEMP_DIR, "doctor_response.wav")
        text_to_speech_with_gtts(
            input_text=doctor_response, 
            output_filepath=output_filepath
        )
        
        # Save conversation history
        conversation_history = [
            ["Patient", speech_to_text_output],
            ["Doctor", doctor_response]
        ]
        
        return speech_to_text_output, doctor_response, output_filepath, conversation_history

    except Exception as e:
        print(f"Error in initial consultation: {str(e)}")
        return f"Error: {str(e)}", "An error occurred during processing", None, []

def chat_with_doctor(message, history):
    """Continue the conversation with the doctor"""
    global conversation_history
    
    try:
        # Get API key
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "Please set a valid GROQ_API_KEY in your .env file"
            
        # Format conversation history for context
        context = format_conversation_context(conversation_history)
            
        # Get doctor's response with conversation context
        doctor_response = query_text_model(
            query=FOLLOWUP_PROMPT + context + f"\nPatient's new question: {message}",
            model="mixtral-8x7b-32768"
        )
        
        # Add to conversation history
        conversation_history.append(["Patient", message])
        conversation_history.append(["Doctor", doctor_response])
        
        return doctor_response

    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return f"I'm sorry, I encountered an error: {str(e)}"