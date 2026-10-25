import sys
import ollama

sys.stdout.write("Hello, Let me think what you are asking :))\n")
sys.stdout.reconfigure(encoding='utf-8')

response = ollama.chat(
    model="Hamid-LFM2.5", 
    messages=[{"role": "user", "content": "Hello, Ollama!"}])

print(response['message']['content'])