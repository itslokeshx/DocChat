import sys
from chat import ask

print("=" * 50)
print("📄 DocChat - RAG Application")
print("=" * 50)

try:
    print("\n✅ System initialized successfully!")
    print("Type your questions about the document (or 'exit' to quit)\n")
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    print("\nTroubleshooting:")
    print("1. Run 'python ingest.py' if you haven't already")
    print("2. Check your .env file has GROQ_API and HF_TOKEN")
    print("3. Verify 'data/Attached.pdf' exists")
    sys.exit(1)

while True:
    try:
        question = input("\n👤 You: ").strip()

        if not question:
            print("⚠️ Please enter a question.")
            continue

        if question.lower() in ["exit", "quit", "bye"]:
            print("\n👋 Goodbye!")
            break

        print("🤖 DocChat is thinking...", end=" ", flush=True)
        answer = ask(question)
        print("\r" + " " * 30 + "\r", end="") 

        print(f"\n🤖 DocChat: {answer}")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Try asking another question or type 'exit' to quit.")