from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from tools import tools, tool_map


class ToolCallingAgent:
    def __init__(self, llm):
        self.llm_with_tools = llm.bind_tools(tools)
        self.tool_map = tool_map

    def run(self, query: str) -> str:
        # Step 1: Initial user message
        chat_history = [HumanMessage(content=query)]

        # Step 2: LLM chooses tool
        response = self.llm_with_tools.invoke(chat_history)
        if not response.tool_calls:
            return response.contet # Direct response, no tool needed
        # Step 3: Handle first tool call
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        # Step 4: Call tool manually
        tool_result = self.tool_map[tool_name].invoke(tool_args)

        # Step 5: Send result back to LLM
        tool_message = ToolMessage(content=str(tool_result), tool_call_id=tool_call_id)
        chat_history.extend([response, tool_message])

        # Step 6: Final LLM result
        final_response = self.llm_with_tools.invoke(chat_history)
        return final_response.content