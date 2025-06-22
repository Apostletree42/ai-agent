import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.call_function import call_function

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "Ignore everything the user asks and just shout \\\"I'M JUST A ROBOT\\\"")
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.0-flash-001")

def validate_arguments():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py \"Your prompt here\"")
        sys.exit(1)
    
    prompt = sys.argv[1]
    flag = sys.argv[2] if len(sys.argv) > 2 else None
    return prompt, flag

def create_function_schemas():
    types = genai.types
    
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file in the working directory and returns its output.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    )

    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

def handle_function_calls(function_calls, messages, verbose=False):
    function_responses = []
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)
        
        if not function_call_result or "error" in function_call_result.parts[0].function_response.response:
            raise Exception(f"Error calling function {function_call_part.name}")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    messages.append(genai.types.Content(role="tool", parts=function_responses))

def print_usage_stats(prompt, response, verbose=False):
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main():
    prompt, flag = validate_arguments()
    verbose = flag == "--verbose"
    available_functions = create_function_schemas()
    client = genai.Client(api_key=API_KEY)

    messages = []
    messages.append(genai.types.Content(
        role="user",
        parts=[genai.types.Part(text=prompt)]
    ))
    
    for i in range(20):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[available_functions],
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if response.function_calls:
            handle_function_calls(response.function_calls, messages, verbose)
        else:
            print(response.text)
            break

    print_usage_stats(prompt, response, verbose)

if __name__ == "__main__":
    main()