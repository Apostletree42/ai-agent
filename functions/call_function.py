from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from google import genai

functions_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

types = genai.types

def call_function(function_call_part, verbose=False):
    if function_call_part.name not in functions_map:
        return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )
    args = function_call_part.args
    args["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    res = functions_map[function_call_part.name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": res},
            )
        ],
    )