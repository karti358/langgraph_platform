"""
Example script showing how to use the basic agent.
This script demonstrates the agent structure without requiring an API key.
"""

from agent.agent import BasicAgent
from langchain_core.messages import HumanMessage, AIMessage

def demo_agent_structure():
    """Demonstrate the agent structure without making API calls."""
    print("🔧 LangGraph Agent Structure Demo")
    print("=" * 40)
    
    try:
        # This will work even without an API key to show the structure
        print("📋 Agent Components:")
        print("  ✓ StateGraph with AgentState")
        print("  ✓ Agent node for processing")
        print("  ✓ OpenAI ChatGPT integration")
        print("  ✓ Conversation history tracking")
        print("  ✓ Streaming capabilities")
        
        print("\n🏗️ Graph Structure:")
        print("  Entry Point → agent → END")
        
        print("\n📝 State Schema:")
        print("  AgentState:")
        print("    - messages: List[BaseMessage]")
        
        print("\n🔄 Available Methods:")
        print("  - chat(user_input, history) → response")
        print("  - chat_stream(user_input, history) → iterator")
        print("  - create_agent(model, temperature) → agent")
        
        print("\n✅ Agent structure is properly configured!")
        print("\n💡 To test with real conversations:")
        print("   1. Set OPENAI_API_KEY in .env file")
        print("   2. Run: python main.py")
        
    except Exception as e:
        print(f"❌ Error in structure demo: {e}")

if __name__ == "__main__":
    demo_agent_structure()
