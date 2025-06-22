import os

def get_files_info(working_directory, directory=None):
    try:
        workpath = os.path.abspath(working_directory)
        direc = os.path.join(workpath, directory) if directory else workpath
        if not direc.startswith(workpath):
            return f'Error: Cannot list "{direc}" as it is outside the permitted working directory'
        if not os.path.isdir(direc):
            return f'Error: "{direc}" is not a directory'
        items = os.listdir(direc)
        res = []
        for item in items:
            itemPath = os.path.join(direc, item)
            size = os.path.getsize(itemPath)
            is_dir = os.path.isdir(itemPath)
            res.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
        return '\n'.join(res)
    except Exception as e:
        print(f'Error: {str(e)}')
    