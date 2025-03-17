import gradio as gr
import sys
import os

# Add the parent directory to sys.path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct imports without the package prefix
from config import setup_environment
from processing import process_initial_consultation, chat_with_doctor
from ui_styles import CUSTOM_CSS, get_header_html, get_footer_html, get_followup_intro_html

def main():
    """Main application entry point"""
    # Setup environment and get basics
    temp_dir, api_key = setup_environment()
    
    # Create the Gradio app with custom theme and styling
    with gr.Blocks(css=CUSTOM_CSS) as app:
        # Header
        with gr.Row(elem_classes=["container"]):
            gr.HTML(get_header_html())
    
        # Main tabs
        with gr.Row(elem_classes=["container", "tabs-container"]):
            with gr.Tab("Initial Consultation", elem_classes=["glass-panel"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Column(elem_classes=["input-container"]):
                            gr.Markdown("### 🎤 Describe Your Symptoms")
                            audio_input = gr.Audio(
                                sources=["microphone"], 
                                type="filepath", 
                                label="Record your voice"
                            )
                        
                        with gr.Column(elem_classes=["input-container"]):
                            gr.Markdown("### 📷 Upload Medical Image")
                            image_input = gr.Image(
                                type="filepath", 
                                label="Upload for diagnosis"
                            )
                        
                        submit_btn = gr.Button("🔍 Get Doctor's Assessment", variant="primary", elem_classes=["primary"])
                        
                    with gr.Column(scale=1):
                        with gr.Column(elem_classes=["output-container"]):
                            speech_text = gr.Textbox(
                                label="Your Symptoms (Transcribed)", 
                                lines=2
                            )
                            
                            doctor_response = gr.Textbox(
                                label="Doctor's Assessment", 
                                lines=5
                            )
                            
                            audio_response = gr.Audio(
                                label="Doctor's Voice Response", 
                                type="filepath",
                                autoplay=True
                            )
                
                with gr.Row():
                    with gr.Column(elem_classes=["chatbot-container"]):
                        consultation_history = gr.Chatbot(
                            label="Consultation Summary",
                            elem_classes=["glass-panel"]
                        )
                
                submit_btn.click(
                    fn=process_initial_consultation,
                    inputs=[audio_input, image_input],
                    outputs=[speech_text, doctor_response, audio_response, consultation_history]
                )
            
            with gr.Tab("Continue Discussion", elem_classes=["glass-panel"]):
                gr.HTML(get_followup_intro_html())
                
                chat_interface = gr.ChatInterface(
                    fn=chat_with_doctor,
                    chatbot=gr.Chatbot(elem_classes=["glass-panel"]),
                    textbox=gr.Textbox(
                        placeholder="Type your follow-up question here...", 
                        container=False, 
                        lines=2
                    )
                )
    
        # Footer
        with gr.Row(elem_classes=["container"]):
            gr.HTML(get_footer_html())
    
        # Launch the app
        print("🏥 Starting AI Doctor application...")
        print(f"🔑 API key status: {'✅ Available' if api_key else '❌ Missing'}")
    
    return app

if __name__ == "__main__": 
    app = main()
    app.launch(
        server_name="127.0.0.1",
        share=False,
        debug=True,
        show_error=True,
       
    )
