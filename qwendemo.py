import ollama

print("🤖 Qwen 3.5 Chatbot (type 'exit' to quit)\n")

conversation = [
    {
        "role": "system",
        "content": "You are a helpful and witty assistant helping Vishal with blogs, coding, Sanskrit, and ideas."
    }
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye! 👋")
        break

    conversation.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="qwen2.5:0.5b",   # 👈 THIS IS YOUR MODEL
        messages=conversation
    )

    bot_reply = response['message']['content']
    print("Bot:", bot_reply)

    conversation.append({"role": "assistant", "content": bot_reply})