import os
from google.genai import types

def write_file(working_directory, file_path, content):
  abs_working_dir = os.path.abspath(working_directory)
  target_path = os.path.abspath(os.path.join(working_directory, file_path))

  if not target_path.startswith(abs_working_dir):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  try:
     with open(target_path, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
     return f'Error: {e}'
  
schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Modifies the contents of a specific file, constrained to the working directory",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The path to the file which we want to write contents to, relative to the working directory.",
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="The contents to write to the file"
      )
    }    
  )
)