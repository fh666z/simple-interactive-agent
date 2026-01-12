# Simple Interactive Agent

A human-in-the-loop tool-calling agent built with LangChain and Google's Gemini model. This project demonstrates how to create an AI agent that asks for user confirmation before executing tools and accepting results.

## Features

- **Interactive confirmations**: User approves each tool call before execution
- **Result validation**: User can accept, retry, or override tool results
- **Multi-step operations**: Handles complex queries requiring multiple tool calls
- **Custom tools**: Math operations (add, subtract, multiply, divide, calculate_tip)
- **Google Gemini integration**: Powered by Google's Gemini 2.5 Flash model

## Project Structure

```
simple-interactive-agent/
├── main.py              # Interactive REPL entry point
├── interacive_agent.py  # InteractiveToolCallingAgent class
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

```python
from langchain.chat_models import init_chat_model
from interacive_agent import InteractiveToolCallingAgent

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
agent = InteractiveToolCallingAgent(llm)

result = agent.run("What is 3 + 5 multiplied by 10?")
```

### Example Session

```
You: What is 3 + 5 multiplied by 10?

========================================
🔧 Tool Call Request (Step 1)
========================================
   Tool: add
   Args: a=3, b=5
========================================
Execute this tool? [y/n]: y

----------------------------------------
📤 Result: 8
----------------------------------------
Accept this result? [y/n]: y

========================================
🔧 Tool Call Request (Step 2)
========================================
   Tool: multiply
   Args: a=8, b=10
========================================
Execute this tool? [y/n]: y

----------------------------------------
📤 Result: 80
----------------------------------------
Accept this result? [y/n]: y

🤖 Agent: 3 + 5 multiplied by 10 equals 80.
```

## Available Tools

| Tool | Description |
|------|-------------|
| `add(a, b)` | Adds two numbers |
| `subtract(a, b)` | Subtracts b from a |
| `multiply(a, b)` | Multiplies two numbers |
| `divide(a, b)` | Divides a by b |
| `calculate_tip(total_bill, tip_percentage)` | Calculates tip amount |

## How It Works

1. User sends a query to the agent
2. The LLM analyzes the query and decides which tool to call
3. **User confirms** whether to execute the tool
4. The agent executes the tool
5. **User accepts** the result (or retries/overrides)
6. Steps 2-5 repeat if more tools are needed
7. The LLM generates a final human-readable response

### Confirmation Flow

- **Tool rejection**: If user declines a tool call, the LLM responds without using tools
- **Result rejection**: 
  - 1st rejection → Retry the tool
  - 2nd rejection → User provides manual override value
  - No override → Operation cancelled

## License

See [LICENSE](LICENSE) for details.
