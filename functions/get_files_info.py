import os
def get_files_info(working_directory, directory="."):
    info_list = []
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        for file_name in os.listdir(target_dir):
            file_path = os.path.normpath(os.path.join(target_dir, file_name))
            info_list.append(f"- {file_name}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
            #- README.md: file_size=1032 bytes, is_dir=False
            #- src: file_size=128 bytes, is_dir=True
            #- package.json: file_size=1234 bytes, is_dir=False
        return "\n".join(info_list)
    except Exception as e:
        return f"Error: {e}"


