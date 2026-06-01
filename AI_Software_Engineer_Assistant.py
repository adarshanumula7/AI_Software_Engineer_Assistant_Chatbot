import panel as pn
from dotenv import load_dotenv
from groq import Groq
import os

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

# endregion

# Initialize the GenAI client
client = Groq(api_key=API_KEY)

# region model definitions
system_prompt = """
You are an AI Software Engineering Assistant. Help users with programming, debugging, algorithms, system design, databases, cloud computing, 
and AI development. Provide clear explanations, code examples when appropriate, and step-by-step solutions. If information is uncertain, 
state the limitations rather than guessing.
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
# AI Software Engineering Assistant
Get detailed notes on any topic you want to learn.
""")

# Design the interface
template = pn.template.FastListTemplate(
    title="AI Software Engineering Assistant",
    sidebar=[
        model_select,
        temperature
    ],
    theme=pn.theme.DarkTheme,
    theme_toggle=False,
    main = [header, 
            chat_ui]
)

template.servable()