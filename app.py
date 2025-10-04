import os
import gradio as gr
from google import genai

# Load API key from environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyABUfFPiweyLapXiMgz_tZ3p5XJsi0VQQg"

# Initialize Gemini client
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# Chat function with history
def chat_with_gemini(user_message, chat_history):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message
        )
        bot_message = response.text
        chat_history.append((user_message, bot_message))
        return chat_history, ""
    except Exception as e:
        chat_history.append((user_message, f"Error: {str(e)}"))
        return chat_history, ""

# Clear chat
def clear_chat():
    return []

# Placeholder functions for Regenerate and Stop
def regenerate(chat_history):
    # Simply remove last AI message so user can resend
    if chat_history:
        chat_history.pop()
    return chat_history

def stop_response(chat_history):
    # Could implement stopping the current generation
    return chat_history

# Gradio Blocks layout
with gr.Blocks(
    css="""
    body { background-color: #cce6ff; }

    /* Center container */
    .gradio-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
    }

    /* Chatbox styling */
    .gr-chatbot-message.user { 
        border: 2px solid #1E90FF !important; 
        border-radius: 12px; 
        padding: 8px; 
        background-color: #cce0ff !important; 
    }
    .gr-chatbot-message.bot { 
        border: 2px solid #1E90FF !important; 
        border-radius: 12px; 
        padding: 8px; 
        background-color: #e6f0ff; 
    }

    /* Input textbox */
    .gr-textbox { 
        border: 2px solid #1E90FF !important; 
        border-radius: 12px !important; 
        padding: 8px; 
        background-color: #cce0ff; 
    }

    /* Button styling */
    .gr-button { 
        background-color: #1E90FF !important; 
        color: white !important; 
        border-radius: 12px !important; 
        padding: 8px 16px; 
        margin-top: 5px;
    }

    /* Chat container scrollable */
    .gr-chatbot-container { 
        max-height: 500px; 
        overflow-y: auto; 
        padding: 10px; 
    }
    """
) as demo:

    # Title
    gr.Markdown("<h1 style='text-align:center;color:#1E90FF;'>AI Chatbot</h1>")

    # Chatbot component
    chatbot = gr.Chatbot(elem_classes="gr-chatbot-container")  

    # Input row
    msg = gr.Textbox(label="Type your message here...", placeholder="Ask me anything!", lines=2)

    # Buttons below input
    with gr.Row():
        clear_btn = gr.Button("Clear Chat")
        regen_btn = gr.Button("Regenerate")
        stop_btn = gr.Button("Stop")

    # Event bindings
    msg.submit(chat_with_gemini, [msg, chatbot], [chatbot, msg])
    clear_btn.click(clear_chat, [], chatbot)
    regen_btn.click(regenerate, chatbot, chatbot)
    stop_btn.click(stop_response, chatbot, chatbot)

demo.launch(share=True)
