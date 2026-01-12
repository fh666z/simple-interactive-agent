# Simple Interactive Agent

A minimal tool-calling agent built with LangChain and Google's Gemini model. This project demonstrates how to create an AI agent that can use custom tools to answer questions.

## Features

- **Tool-calling agent**: Uses LangChain's tool-calling capabilities to invoke custom functions
- **Custom tools**: Includes basic math operations (add, subtract, multiply)
- **Google Gemini integration**: Powered by Google's Gemini 2.5 Flash model

## Project Structure

```
simple-interactive-agent/
├── main.py              # Entry point for testing the agent
├── interacive_agent.py  # ToolCallingAgent class definition
├── tools.py             # Custom tool definitions
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Google API key:**
   
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   
   Or export it directly:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

3. **Run the agent:**
   ```bash
   python main.py
   ```

## Usage

The agent can answer math questions by using the available tools:

```python
from langchain.chat_models import init_chat_model
from interacive_agent import ToolCallingAgent

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
agent = ToolCallingAgent(llm)

result = agent.run("What is 3 + 5?")
print(result)  # Output: 8
```

## Available Tools

| Tool | Description |
|------|-------------|
| `add(a, b)` | Adds two integers |
| `subtract(a, b)` | Subtracts b from a |
| `multiply(a, b)` | Multiplies two integers |

## How It Works

1. User sends a query to the agent
2. The LLM analyzes the query and decides which tool to call
3. The agent executes the tool with the provided arguments
4. The tool result is sent back to the LLM
5. The LLM generates a final human-readable response

## License

See [LICENSE](LICENSE) for details.
