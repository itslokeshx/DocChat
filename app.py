from chat import ask

print("=" * 50)
print("DocChat")
print("=" * 50)

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    answer = ask(question)

    print("\nDocChat :", answer)