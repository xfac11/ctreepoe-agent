import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import*
def generate_content(client, model_name, contents, config):
    return client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config
        )
    
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
    model_name = 'gemini-2.5-flash'
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini api key wasn't found")

    client = genai.Client(api_key=api_key)
    if client == None:
        raise RuntimeError("Genai couldn't create a client")
    config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions],
    )

    function_results = []
    messages = [types.Content(role="user", parts=parts)]

    for _ in range(20):
        response = generate_content(client, model_name, messages, config)
        if response.usage_metadata == None:
            raise RuntimeError(
                "usage_metadata was None, likely a failed API request"
            )
        candidates = response.candidates
        if len(candidates) == 0:
            raise Exception("Found no candidates (it should be)")
        for candidate in candidates:
            messages.append(candidate.content)
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
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
            return
        
        messages.append(types.Content(role="user", parts=function_results))
    
    print("Cannot solve the issue")
    exit(1)


if __name__ == "__main__":
    main()
