import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
  abs_working_dir = os.path.abspath(working_directory)
  target_path = os.path.abspath(os.path.join(working_directory, file_path))

  if not target_path.startswith(abs_working_dir):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(target_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'
  
  try:
    file_content_string = ''

    with open(target_path, "r") as f:
      file_content_string = f.read(MAX_CHARS) 

    if os.path.getsize(target_path) > MAX_CHARS:
      file_content_string = f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'

    return file_content_string
  except Exception as e:
    return f'Error: {e}'
  
schema_get_file_content = types.FunctionDeclaration(
  name="get_file_content",
  description="Gets the contents of a specific file, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The path to the file which contents we want to read, relative to the working directory.",
      ),
    },
  ),
)