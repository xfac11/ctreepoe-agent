import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]
        if args is not None:
            command.extend(args)
        
        completed_process = subprocess.run(
            command, 
            text=True,
            capture_output=True,
            cwd=working_dir_abs,
            timeout=30.0
        )

        return_code = completed_process.returncode
        stdout = completed_process.stdout
        stderr = completed_process.stderr

        output = "" if return_code == 0 else f"Process exited with code {return_code}\n"
        if stdout == None and stderr == None:
            output += "No output produced\n"
        else:
            output += f"STDOUT:{stdout}\n"
            output += f"STDERR:{stderr}\n"
        
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    