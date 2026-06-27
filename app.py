from chat import ask

print("=" * 50)
print("📄 DocChat")
print("=" * 50)

while True:

    question = input("\nYou : ")

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    answer = ask(question)

    print(f"\nDocChat : {answer}")