# Custom CSS for dark blue and black theme
CUSTOM_CSS = """
:root {
    --primary-color: #0c4a6e;       /* Darker blue */
    --secondary-color: #0284c7;     /* Medium blue */
    --accent-color: #38bdf8;        /* Bright blue for highlights */
    --background-color: #020617;    /* Almost black background */
    --surface-color: rgba(15, 23, 42, 0.90); /* Dark blue-black surface */
    --text-color: #e2e8f0;          /* Light gray text */
    --border-color: rgba(51, 65, 85, 0.5); /* Slightly brighter borders */
    --highlight-color: rgba(14, 165, 233, 0.15); /* Blue highlight */
}

body {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
    background-image: 
        radial-gradient(circle at 25% 25%, rgba(12, 74, 110, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 75% 75%, rgba(14, 165, 233, 0.1) 0%, transparent 50%);
    background-attachment: fixed;
}

.gradio-container {
    background-color: transparent !important;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.glass-panel {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.glass-panel:hover {
    box-shadow: 0 8px 32px 0 rgba(14, 165, 233, 0.2);
    border-color: rgba(56, 189, 248, 0.3);
}

.header-text {
    color: var(--accent-color);
    text-align: center;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: 16px;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    font-size: 1.5rem;
    letter-spacing: 1px;
}

.input-container {
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 15px;
    background-color: rgba(2, 6, 23, 0.8); /* Near black */
    margin-bottom: 15px;
    transition: all 0.3s ease;
}

.input-container:hover {
    border-color: rgba(56, 189, 248, 0.4);
    box-shadow: 0 0 15px rgba(14, 165, 233, 0.1);
}

.output-container {
    border-left: 3px solid var(--accent-color);
    padding-left: 15px;
    background-color: rgba(2, 6, 23, 0.7); /* Near black but lighter */
    border-radius: 0 8px 8px 0;
    transition: all 0.3s ease;
}

.output-container:hover {
    border-left-color: var(--secondary-color);
    box-shadow: 0 0 10px rgba(14, 165, 233, 0.1);
}

.chatbot-container {
    border-radius: 12px;
    overflow: hidden;
    background-color: rgba(15, 23, 42, 0.7); /* Dark blue */
}

button.primary {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2) !important;
    filter: brightness(1.1) !important;
}

button.primary:active {
    transform: translateY(1px) !important;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2) !important;
}

/* Message bubbles in chat */
.message {
    border-radius: 10px !important;
    padding: 12px !important;
    margin-bottom: 10px !important;
}

.user-message {
    background-color: rgba(51, 65, 85, 0.8) !important; /* Dark blue-gray */
    border-top-right-radius: 2px !important;
}

.bot-message {
    background-color: rgba(12, 74, 110, 0.8) !important; /* Dark blue */
    border-top-left-radius: 2px !important;
}

/* Tabs styling */
.tabs > .tab-nav > button {
    color: var(--text-color) !important;
    border-radius: 8px 8px 0 0 !important;
    background-color: transparent !important;
}

.tabs > .tab-nav > button.selected {
    border-bottom: 2px solid var(--accent-color) !important;
    color: var(--accent-color) !important;
    background-color: rgba(14, 165, 233, 0.1) !important;
}

/* Glowing accent effects */
.glow-effect {
    position: relative;
}

.glow-effect::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(14, 165, 233, 0.3);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.glow-effect:hover::after {
    opacity: 1;
}

/* Greeting section */
.greeting-container {
    margin-bottom: 20px;
}

.greeting-panel {
    background: linear-gradient(to right, rgba(2, 6, 23, 0.9), rgba(12, 74, 110, 0.8));
    border-left: 4px solid var(--secondary-color);
}

.greeting-audio {
    margin-top: 10px;
    background: rgba(2, 6, 23, 0.8);
    border-radius: 8px;
    padding: 10px;
}

@keyframes pulse-highlight {
    0% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(14, 165, 233, 0); }
    100% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }
}

.greeting-panel {
    animation: pulse-highlight 2s ease-out 1;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: rgba(56, 189, 248, 0.4);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(56, 189, 248, 0.6);
}
"""

def get_header_html():
    """Return the HTML for the app header"""
    return """
    <div class="glass-panel glow-effect">
        <h1 class="header-text">🏥 AI Doctor Consultation</h1>
        <p style="text-align: center; margin-bottom: 0; opacity: 0.9;">Get professional medical assessment using AI-powered diagnosis</p>
        <div style="text-align: center; margin-top: 15px;">
            <span style="display: inline-block; width: 8px; height: 8px; 
                  background-color: #38bdf8; border-radius: 50%; margin-right: 5px; 
                  box-shadow: 0 0 8px #38bdf8;"></span>
            <span style="font-size: 0.8em; opacity: 0.8;">System Online</span>
        </div>
    </div>
    """

def get_footer_html():
    """Return the HTML for the app footer"""
    return """
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(51, 65, 85, 0.5); color: #64748b;">
        <p>AI Doctor Application - For educational purposes only</p>
        <p style="font-size: 0.8em; opacity: 0.7;">This is not a substitute for professional medical advice.</p>
        <div style="margin-top: 15px; font-size: 0.8em;">
            <span style="color: #38bdf8;">&#9679;</span> Privacy Protected 
            <span style="margin: 0 10px;">|</span>
            <span style="color: #38bdf8;">&#9679;</span> HIPAA Compliant
            <span style="margin: 0 10px;">|</span>
            <span style="color: #38bdf8;">&#9679;</span> Secure Communication
        </div>
    </div>
    """

def get_followup_intro_html():
    """Return the HTML for the follow-up tab intro"""
    return """
    <div class="glass-panel">
        <h3 style="color: var(--accent-color); margin-top: 0;">💬 Continue your conversation with the doctor</h3>
        <p>After your initial consultation, you can ask follow-up questions here.</p>
        <div style="background-color: rgba(14, 165, 233, 0.1); border-left: 3px solid var(--accent-color); 
                    padding: 10px; margin-top: 15px; border-radius: 0 6px 6px 0;">
            <p style="margin: 0; font-size: 0.9em;">
                <strong>Tip:</strong> Be specific with your symptoms and questions to receive the most accurate guidance.
            </p>
        </div>
    </div>
    """