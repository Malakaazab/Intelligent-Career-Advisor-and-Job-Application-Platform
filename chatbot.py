import google.generativeai as genai

genai.configure(api_key="AIzaSyAMTVtoQV5DJIaKHok_xT9RoQSt1MlAWeA")

print("Type your question:(or type'exit' to quit):")

while True:
    userPrompt = input("you: ")

    if userPrompt.lower() == "exit":
        print("goodbye")
        break
    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(f"Answer briefly and clearly: {userPrompt}")

    print("AI: ", response.text)