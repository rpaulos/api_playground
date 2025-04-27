from openai import OpenAI
from sk import my_sk
import time

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=my_sk)

complete_this = input("Prompt: ")

# Create a chat completion
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": complete_this}]
)

# Print the output
print(chat_completion.choices[0].message.content)
print()
print(dir(OpenAI))