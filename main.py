import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import*
def main():
    load_dotenv()
    print("Hello from ctreepoe-agent!")
    parser = argparse.ArgumentParser(
        description="ctreepoe-agent - A helping chat bot"
    )
    parser.add_argument(
        "user_prompt",
        type=str,
        help="The message to the helpful chat bot"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()
    parts=[types.Part(text=args.user_prompt)]
    messages = [types.Content(role="user", parts=parts)]
    model_name = 'gemini-2.5-flash'
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini api key wasn't found")

    client = genai.Client(api_key=api_key)
    if client == None:
        raise RuntimeError("Genai couldn't create a client")

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions],
        ),
    )
    if response.usage_metadata == None:
        raise RuntimeError(
            "usage_metadata was None, likely a failed API request"
            )
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    function_results = []
    if response.function_calls != None:
        for call in response.function_calls:
            function_call_result = call_function(call, True)
            if len(function_call_result.parts) == 0:
                raise Exception("Function call Parts list was empty")
            function_response = function_call_result.parts[0].function_response
            if function_response == None:
                raise Exception("Parts[0] function response in function call result was None")
            if function_response.response == None:
                raise Exception("The function response response was None")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
