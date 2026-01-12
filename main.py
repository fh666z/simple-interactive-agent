from langchain.chat_models import init_chat_model
from interacive_agent import InteractiveToolCallingAgent


def main():
    # Initialize the LLM
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    
    # Create the interactive agent
    agent = InteractiveToolCallingAgent(llm)
    
    print("=" * 50)
    print("🤖 Interactive Tool-Calling Agent")
    print("=" * 50)
    print("Type your questions. Type 'quit' to exit.\n")
    
    while True:
        query = input("You: ").strip()
        
        if not query:
            continue
        
        if query.lower() in ('quit', 'exit', 'q'):
            print("Goodbye! 👋")
            break
        
        result = agent.run(query)
        print(f"\n🤖 Agent: {result}\n")


if __name__ == "__main__":
    main()
