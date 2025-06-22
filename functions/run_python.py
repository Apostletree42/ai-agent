import os
import subprocess


def run_python_file(working_directory, file_path):
    try:
        workpath = os.path.abspath(working_directory)
        direc = os.path.join(workpath, file_path) if file_path else workpath
        abs_path = os.path.abspath(direc)
        if not abs_path.startswith(workpath):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        res = subprocess.run(
            ['python3', abs_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=workpath
        )

        op = []
        if res.stdout:
            op.append(f'STDOUT:\n{res.stdout}')
        if res.stderr:
            op.append(f'STDERR:\n{res.stderr}')
        if res.returncode != 0:
            op.append(f'Process exited with code {res.returncode}')
        if not op:
            return 'No output produced.'

        return '\n'.join(op)
    except Exception as e:
        return f'Error: {str(e)}'