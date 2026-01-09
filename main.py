import os
import argparse
from dotenv import load_dotenv
from google import genai
def main():
    print("Hello from ctreepoe-agent!")
    parser = argparse.ArgumentParser(description="ctreepoe-agent - A helping chat bot")
    parser.add_argument("user_prompt", type=str, help="The message to the helpful chat bot")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini api key wasn't found")

    client = genai.Client(api_key=api_key)
    if client == None:
        raise RuntimeError("Genai couldn't create a client")

    response = client.models.generate_content(model='gemini-2.5-flash', contents=args.user_prompt)
    if response.usage_metadata == None:
        raise RuntimeError("usage_metadata was None, likely a failed API request")
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)



if __name__ == "__main__":
    main()
