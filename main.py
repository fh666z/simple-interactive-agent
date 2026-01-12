from langchain.chat_models import init_chat_model
from interacive_agent import ToolCallingAgent


def main():
    # Initialize the LLM
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    
    # Create the agent
    agent = ToolCallingAgent(llm)
    
    # Test queries
    queries = [
        "What is 3 + 5?",
        "What is 10 - 4?",
        "What is 6 * 7?",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = agent.run(query)
        print(f"Answer: {result}")


if __name__ == "__main__":
    main()
