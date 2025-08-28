import os
from agent.agent import create_agent
from langchain_core.messages import HumanMessage, AIMessage

def main():
    """Main function to demonstrate the basic agent."""
    print("🤖 LangGraph Basic Agent Demo")
    print("=" * 40)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        return
    
    # Create the agent
    try:
        agent = create_agent(model_name="gpt-3.5-turbo", temperature=0.7)
        print("✅ Agent created successfully!")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return
    
    # Interactive chat loop
    print("\n💬 Chat with the agent (type 'quit' to exit):")
    print("-" * 40)
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit condition
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Get agent response
            print("🤖 Agent: ", end="", flush=True)
            
            # Use streaming for better UX
            response_content = ""
            for chunk in agent.chat_stream(user_input, conversation_history):
                print(chunk, end="", flush=True)
                response_content += chunk
            
            print()  # New line after streaming
            
            # Update conversation history
            conversation_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=response_content)
            ])
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

def demo_simple_chat():
    """Simple demo without interactive loop."""
    print("🔧 Running simple demo...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is not set.")
        return
    
    try:
        # Create agent
        agent = create_agent()
        
        # Simple conversation
        questions = [
            "Hello! What can you help me with?",
            "What is the capital of France?",
            "Can you explain what you are in simple terms?"
        ]
        
        conversation_history = []
        
        for question in questions:
            print(f"\n👤 User: {question}")
            response = agent.chat(question, conversation_history)
            print(f"🤖 Agent: {response}")
            
            # Update history
            conversation_history.extend([
                HumanMessage(content=question),
                AIMessage(content=response)
            ])
            
    except Exception as e:
        print(f"❌ Error in demo: {e}")

if __name__ == "__main__":
    # You can switch between interactive and demo mode
    interactive_mode = True
    
    if interactive_mode:
        main()
    else:
        demo_simple_chat()
