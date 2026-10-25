import sys
import ollama

# Write a welcome message to the terminal
sys.stdout.write("Hello, Let me think what you are asking :))\n")

# Set terminal output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Send a chat request to the Ollama model
response = ollama.chat(
    model="Hamid-LFM2.5", 
    messages=[{"role": "user", "content": "Hello, Ollama!"}]
)

# Print the model's response text
print(response['message']['content'])
