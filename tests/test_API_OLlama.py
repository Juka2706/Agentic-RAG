from dotenv import load_dotenv
load_dotenv()

import openai

# 1. Initialize the OpenAI client
# We must point the client to your local Ollama server
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",  # The default Ollama API endpoint
    api_key="API_KEY_OLLAMA"  # API key is required by the client, but Ollama ignores it
)

# 2. Define your model and messages
model_to_use = "gemma3:27b"
messages = [
    {
        "role": "user",
        "content": "Hi, I am trying the API Key"
    }
]

# 3. Make the API request
try:
    response = client.chat.completions.create(
        model=model_to_use,
        messages=messages,
        stream=False  # Set to False for a single, complete response
    )

    # 4. Print the assistant's reply
    print("--- Ollama's Response ---")
    print(response.choices[0].message.content)

except openai.RateLimitError:
    print("Rate limit exceeded. (This shouldn't happen with a local server)")
except openai.APIConnectionError:
    print(f"Error: Could not connect to the server at {client.base_url}")
    print("Please ensure your Ollama server is running.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")