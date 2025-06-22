import os

def write_file(working_directory, file_path, content):
    try:
        workpath = os.path.abspath(working_directory)
        direc = os.path.join(workpath, file_path) if file_path else workpath
        abs_path = os.path.abspath(direc)
        if not abs_path.startswith(workpath):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        with open(abs_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'