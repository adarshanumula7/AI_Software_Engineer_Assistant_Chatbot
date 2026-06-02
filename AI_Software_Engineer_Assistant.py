import panel as pn
from dotenv import load_dotenv
from groq import Groq
import os
import io, json

pn.extension()
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# region helper methods
def get_response_from_messages(chat_history, model="llama-3.3-70b-versatile", temperature=0):
    messages = [
        {"role": "system", "content": system_prompt},
        *chat_history
    ]
    # print("Before Groq call")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    # print("After Groq call")
    return response.choices[0].message.content

def chat_callback(message, user, instance):
    try: 
        chat_history.append({"role": "user", "content": message})
        # print("Entered Chat Callback")
        # prompt = f"{system_prompt}\n\n" + "\n".join(chat_history)
        response = get_response_from_messages(chat_history, model=model_select.value, temperature=temperature.value)
        # print("Got response from get_response_from_messages")
        chat_history.append({"role": "assistant", "content": response})
        # print(chat_history)
        return response
    except Exception as e:
        print("ERROR: ", repr(e))
        raise

def generate_chat_json():
    json_str = json.dumps(chat_history, indent=2)
    return io.StringIO(json_str)

def generate_txt():
    text = ""

    for msg in chat_history:
        text += f"{msg['role'].capitalize()}:\n"
        text += f"{msg['content']}\n\n"

    return io.StringIO(text)

# endregion 

# region UI details
temperature = pn.widgets.FloatSlider(
    name="Temperature",
    start=0,
    end=2,
    step=0.1,
    value=0.7
)

model_select = pn.widgets.Select(
    name="Model",
    options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    value="llama-3.3-70b-versatile"
)

download_button = pn.widgets.FileDownload(
    filename="chat_history.txt",
    button_type="primary",
    label="Download Chat History",
    sizing_mode="stretch_width",
    callback=generate_txt
)
# endregion

# Initialize the GenAI client
client = Groq(api_key=API_KEY)

# region model definitions
system_prompt = """
You are an expert Software Engineer, AI Engineer, Technical Mentor, and System Design Consultant.

Your responsibilities are:

1. Provide accurate software engineering guidance.
2. Explain concepts step-by-step.
3. Generate clean, production-quality code.
4. Follow software engineering best practices.
5. Suggest performance, scalability, and security improvements.
6. Ask clarifying questions when requirements are ambiguous.
7. Explain trade-offs between different approaches.
8. Use markdown formatting.
9. Use code blocks for code examples.
10. Never invent APIs, libraries, or facts.

Response Style:
- Professional
- Clear
- Practical
- Concise
- Educational

When providing code:
- Include comments when useful.
- Mention complexity when relevant.
- Highlight security considerations.
- Suggest testing approaches.
"""
# endregion

# Display chat interface
chat_ui = pn.chat.ChatInterface(
    callback=chat_callback,
    sizing_mode="stretch_width",
    height=600,
    message_params={
        "styles": {
            "background": "#2b2b2b",
            "color": "white"
        }
    }
)

chat_history = []  # This will store the conversation history

pn.extension(
    raw_css=[
        """
        button[aria-label="Toggle the Sidebar"]::after {
            display: none !important;
        }
        .message {
            color: black !important;
        }

        .message-content {
            color: black !important;
        }

        .message-content p,
        .message-content li,
        .message-content span {
            color: black !important;
        }
        """
    ]
)

header = pn.pane.Markdown("""
# 🤖 AI Software Engineering Assistant

A conversational AI application powered by **Groq LLMs** and built with **Panel**.

### Features
- Software Engineering Guidance
- Code Generation & Review
- Debugging Assistance
- System Design Support
- AI & LLM Development Help
- Technical Interview Preparation

Designed to demonstrate practical skills in:
**LLM Integration • Prompt Engineering • Python • Docker • CI/CD • Hugging Face Deployment**
""")

# Design the interface

settings = pn.Card(
    model_select,
    temperature,
    title="Generation Settings"
)

export = pn.Card(
    download_button,
    title="Export"
)

template = pn.template.FastListTemplate(
    title="AI Software Engineering Assistant",
    sidebar=[
        settings,
        pn.Spacer(height=20),
        export
    ],
    theme=pn.theme.DarkTheme,
    theme_toggle=False,
    main = [header, 
            chat_ui]
)

template.servable()