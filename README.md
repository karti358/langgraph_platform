# LangGraph Platform - Basic Agent

A basic conversational agent built with LangChain, LangGraph, and OpenAI.

## Features

- 🤖 Basic conversational AI agent using OpenAI's GPT models
- 🔄 State management with LangGraph
- 💬 Interactive chat interface
- 🔄 Streaming responses for better user experience
- 📝 Conversation history tracking

## Setup

1. **Clone and navigate to the project:**
   ```bash
   cd langgraph_platform
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Interactive Chat

Run the main script for an interactive chat session:

```bash
python main.py
```

### Programmatic Usage

You can also use the agent programmatically:

```python
from agent.agent import create_agent

# Create an agent
agent = create_agent(model_name="gpt-3.5-turbo", temperature=0.7)

# Simple chat
response = agent.chat("Hello, how are you?")
print(response)

# Chat with conversation history
from langchain_core.messages import HumanMessage, AIMessage

history = [
    HumanMessage(content="My name is Alice"),
    AIMessage(content="Nice to meet you, Alice!")
]

response = agent.chat("What's my name?", conversation_history=history)
print(response)  # Should remember your name is Alice

# Streaming chat
for chunk in agent.chat_stream("Tell me a short story"):
    print(chunk, end="", flush=True)
```

## Project Structure

```
langgraph_platform/
├── agent/
│   ├── __init__.py
│   └── agent.py          # Main agent implementation
├── main.py               # Interactive demo
├── pyproject.toml        # Dependencies
├── .env.example          # Environment variables template
└── README.md
```

## How It Works

The agent is built using:

1. **LangChain OpenAI**: For interfacing with OpenAI's GPT models
2. **LangGraph**: For managing conversation state and flow
3. **State Management**: Tracks conversation history using typed dictionaries
4. **Streaming**: Provides real-time response streaming for better UX

The agent uses a simple state graph with a single node that:
- Takes the current conversation state
- Processes it through the OpenAI model
- Returns the updated state with the new response

## Requirements

- Python 3.11+
- OpenAI API key
- Dependencies listed in `pyproject.toml`

## License

This project is licensed under the terms specified in the LICENSE file.