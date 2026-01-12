from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model

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
        return ''.join(
            block.get('text', '') if isinstance(block, dict) and block.get('type') == 'text'
            else block if isinstance(block, str) else ''
            for block in content
        )
    
    return str(content)


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
            response = self.llm_with_tools.invoke(chat_history)
            
            if not response.tool_calls:
                return extract_text_content(response.content)
            
            step += 1
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            if not self._confirm_tool_call(tool_name, tool_args, step):
                return self._handle_tool_rejection(chat_history)

            accepted_result = self._execute_with_confirmation(tool_name, tool_args)
            
            if accepted_result is None:
                return "❌ Operation cancelled by user."

            tool_message = ToolMessage(content=str(accepted_result), tool_call_id=tool_call_id)
            chat_history.extend([response, tool_message])

    def _prompt_yes_no(self, prompt: str) -> bool:
        """Prompt user for yes/no input."""
        while True:
            choice = input(prompt).strip().lower()
            if choice in ('y', 'yes'):
                return True
            if choice in ('n', 'no'):
                return False
            print("Please enter 'y' or 'n'.")

    def _confirm_tool_call(self, tool_name: str, tool_args: dict, step: int = 1) -> bool:
        """Ask user to confirm before executing tool."""
        print("\n" + "=" * 40)
        print(f"🔧 Tool Call Request (Step {step})")
        print("=" * 40)
        print(f"   Tool: {tool_name}")
        print(f"   Args: {self._format_args(tool_args)}")
        print("=" * 40)
        return self._prompt_yes_no("Execute this tool? [y/n]: ")

    def _confirm_tool_result(self, result) -> bool:
        """Ask user to accept/reject the tool result."""
        print("\n" + "-" * 40)
        print(f"📤 Result: {result}")
        print("-" * 40)
        return self._prompt_yes_no("Accept this result? [y/n]: ")

    def _execute_with_confirmation(self, tool_name: str, tool_args: dict):
        """
        Execute tool with confirmation and retry logic.
        
        Returns:
            The accepted result, or None if user cancels.
        """
        for attempt in range(1, self.MAX_RETRIES + 1):
            tool_result = self.tool_map[tool_name].invoke(tool_args)
            
            if self._confirm_tool_result(tool_result):
                return tool_result
            
            if attempt < self.MAX_RETRIES:
                print(f"\n🔄 Retrying... (attempt {attempt + 1}/{self.MAX_RETRIES})")
        
        return self._ask_for_override()

    def _ask_for_override(self):
        """Ask user to provide a manual override value."""
        print("\n" + "=" * 40)
        print("📝 Manual Override")
        print("=" * 40)
        print("You've rejected the result twice.")
        print("Enter a manual value, or leave empty to cancel.")
        
        return input("Override value: ").strip() or None

    def _handle_tool_rejection(self, chat_history: list) -> str:
        """Handle when user rejects tool call - ask LLM to respond without tools."""
        decline_message = HumanMessage(
            content="I don't want to use any tools. Please respond directly without using tools."
        )
        chat_history.append(decline_message)
        
        llm_without_tools = self.llm_with_tools.bound
        final_response = llm_without_tools.invoke(chat_history)
        return extract_text_content(final_response.content)

    def _format_args(self, args: dict) -> str:
        """Format tool arguments for display."""
        return ", ".join(f"{k}={v}" for k, v in args.items())
