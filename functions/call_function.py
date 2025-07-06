from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORKING_DIR

available_functions = types.Tool(
  function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
  ]
)

def call_function(function_call_part, verbose=False):
  if verbose:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  name_to_function = {
    'get_file_content': get_file_content,
    'get_files_info': get_files_info,
    'run_python_file': run_python_file,
    'write_file': write_file
  }

  function_name = function_call_part.name

  if function_call_part.name not in name_to_function:
    return types.Content(
      role="tool",
      parts=[
        types.Part.from_function_response(
          name=function_name,
          response={"error": f"Unknown function: {function_name}"},
        )
      ],
    )
  
  args = dict(function_call_part.args)
  args["working_directory"] = WORKING_DIR
  result = name_to_function[function_name](**args)
  return types.Content(
    role="tool",
    parts=[
      types.Part.from_function_response(
        name=function_name,
        response={"result": result},
      )
    ],
  )