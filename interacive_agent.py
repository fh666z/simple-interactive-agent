from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from tools import tools, tool_map


def extract_text_content(content) -> str:
    """
    Extract text from LLM response content.
    
    Handles both plain strings and list of content blocks
    (e.g., [{'type': 'text', 'text': '...'}]).
    """
    if isinstance(content, str):
        return content
    
    if isinstance(content, list):
        # Extract text from content blocks
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                texts.append(block.get('text', ''))
            elif isinstance(block, str):
                texts.append(block)
        return ''.join(texts)
    
    # Fallback: convert to string
    return str(content)


class ToolCallingAgent:
    """Original autonomous agent (no confirmations)."""
    
    def __init__(self, llm):
        self.llm_with_tools = llm.bind_tools(tools)
        self.tool_map = tool_map

    def run(self, query: str) -> str:
        chat_history = [HumanMessage(content=query)]

        response = self.llm_with_tools.invoke(chat_history)
        if not response.tool_calls:
            return extract_text_content(response.content)
        
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        tool_result = self.tool_map[tool_name].invoke(tool_args)

        tool_message = ToolMessage(content=str(tool_result), tool_call_id=tool_call_id)
        chat_history.extend([response, tool_message])

        final_response = self.llm_with_tools.invoke(chat_history)
        return extract_text_content(final_response.content)


class InteractiveToolCallingAgent:
    """Interactive agent with human-in-the-loop confirmations."""
    
    MAX_RETRIES = 2  # After 2 rejections, ask for manual override
    
    def __init__(self, llm):
        self.llm_with_tools = llm.bind_tools(tools)
        self.tool_map = tool_map

    def run(self, query: str) -> str:
        chat_history = [HumanMessage(content=query)]
        step = 0

        while True:
            # Get LLM response
            response = self.llm_with_tools.invoke(chat_history)
            
            # If no tool calls, we're done - return final response
            if not response.tool_calls:
                return extract_text_content(response.content)
            
            step += 1
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            # Confirm tool execution
            if not self._confirm_tool_call(tool_name, tool_args, step):
                return self._handle_tool_rejection(chat_history, response)

            # Execute tool and confirm result (with retry logic)
            accepted_result = self._execute_with_confirmation(tool_name, tool_args)
            
            if accepted_result is None:
                return "❌ Operation cancelled by user."

            # Add response and tool result to chat history, then loop for next step
            tool_message = ToolMessage(content=str(accepted_result), tool_call_id=tool_call_id)
            chat_history.extend([response, tool_message])

    def _confirm_tool_call(self, tool_name: str, tool_args: dict, step: int = 1) -> bool:
        """Ask user to confirm before executing tool."""
        print("\n" + "=" * 40)
        print(f"🔧 Tool Call Request (Step {step})")
        print("=" * 40)
        print(f"   Tool: {tool_name}")
        print(f"   Args: {self._format_args(tool_args)}")
        print("=" * 40)
        
        while True:
            choice = input("Execute this tool? [y/n]: ").strip().lower()
            if choice in ('y', 'yes'):
                return True
            elif choice in ('n', 'no'):
                return False
            else:
                print("Please enter 'y' or 'n'.")

    def _confirm_tool_result(self, result) -> bool:
        """Ask user to accept/reject the tool result."""
        print("\n" + "-" * 40)
        print(f"📤 Result: {result}")
        print("-" * 40)
        
        while True:
            choice = input("Accept this result? [y/n]: ").strip().lower()
            if choice in ('y', 'yes'):
                return True
            elif choice in ('n', 'no'):
                return False
            else:
                print("Please enter 'y' or 'n'.")

    def _execute_with_confirmation(self, tool_name: str, tool_args: dict):
        """
        Execute tool with confirmation and retry logic.
        
        Returns:
            The accepted result, or None if user cancels.
        """
        attempts = 0
        
        while attempts < self.MAX_RETRIES:
            attempts += 1
            
            # Execute the tool
            tool_result = self.tool_map[tool_name].invoke(tool_args)
            
            # Ask for confirmation
            if self._confirm_tool_result(tool_result):
                return tool_result
            
            # User rejected - show retry message
            if attempts < self.MAX_RETRIES:
                print(f"\n🔄 Retrying... (attempt {attempts + 1}/{self.MAX_RETRIES})")
        
        # Max retries reached - ask for manual override
        return self._ask_for_override()

    def _ask_for_override(self):
        """Ask user to provide a manual override value."""
        print("\n" + "=" * 40)
        print("📝 Manual Override")
        print("=" * 40)
        print("You've rejected the result twice.")
        print("Enter a manual value, or leave empty to cancel.")
        
        override = input("Override value: ").strip()
        
        if override:
            return override
        return None

    def _handle_tool_rejection(self, chat_history: list, response) -> str:
        """Handle when user rejects tool call - ask LLM to respond without tools."""
        # Add context that user declined the tool
        decline_message = HumanMessage(
            content="I don't want to use any tools. Please respond directly without using tools."
        )
        chat_history.append(decline_message)
        
        # Get LLM response without tool binding
        llm_without_tools = self.llm_with_tools.bound  # Get the base LLM
        final_response = llm_without_tools.invoke(chat_history)
        return extract_text_content(final_response.content)

    def _format_args(self, args: dict) -> str:
        """Format tool arguments for display."""
        return ", ".join(f"{k}={v}" for k, v in args.items())
