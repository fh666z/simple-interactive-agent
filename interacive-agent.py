from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

@tool
def add(a: int, b: int) -> int:
    """
    Add a and b.
    
    Args:
        a (int): first integer to be added
        b (int): second integer to be added

    Return:
        int: sum of a and b
    """
    return a + b

@tool
def subtract(a: int, b:int) -> int:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: int, b:int) -> int:
    """Multiply a and b."""
    return a * b

tools = [add, subtract, multiply]
tool_map = {
    "add": add, 
    "subtract": subtract,
    "multiply": multiply
}
llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")


llm_with_tools = llm.bind_tools(tools)

query = "What is 3 + 2?"
chat_history = [HumanMessage(content=query)]

response_1 = llm_with_tools.invoke(chat_history)
chat_history.append(response_1)

#print(type(response_1))
#response_1.pretty_print()

tool_calls_1 = response_1.tool_calls

tool_1_name = tool_calls_1[0]["name"]
tool_1_args = tool_calls_1[0]["args"]
tool_call_1_id = tool_calls_1[0]["id"]

tool_response = tool_map[tool_1_name].invoke(tool_1_args)
tool_message = ToolMessage(content=tool_response, tool_call_id=tool_call_1_id)

chat_history.append(tool_message)

answer = llm_with_tools.invoke(chat_history)
print(type(answer))
print(answer.content)