import os

def get_file_content(working_directory, file_path):
    try:
        workpath = os.path.abspath(working_directory)
        direc = os.path.join(workpath, file_path) if file_path else workpath
        abs_path = os.path.abspath(direc)
        if not abs_path.startswith(workpath):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_path) as file:
            content = file.read()
            if len(content) > 10000:
                content = content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f'Error: {str(e)}'
    