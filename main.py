import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function, available_functions

if len(sys.argv) < 2:
  print("Error: Missing prompt argument pos 1")
  exit(1)

prompt = sys.argv[1]
verbose = "--verbose" in sys.argv
messages = [ types.Content(role="user", parts=[types.Part(text=prompt)]), ]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Run python files
- Write files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
content_response = client.models.generate_content(
  model="gemini-2.0-flash-001",
  contents=messages,
  config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

if content_response.function_calls:
  for f_call in content_response.function_calls:
    result = call_function(f_call, verbose=verbose)
    
    if not result.parts[0].function_response.response:
      raise Exception('Result missing parts')
    
    if verbose:
      print(f"-> {result.parts[0].function_response.response}")
else:
  print(content_response.text)

if verbose:
  print(f"User prompt: {prompt}")
  print(f"Prompt tokens: {content_response.usage_metadata.prompt_token_count}")
  print(f"Response tokens: {content_response.usage_metadata.candidates_token_count}")