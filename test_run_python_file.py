from functions.run_python_file import run_python_file
def main():
    
    #test_cases = [
     #   {"cwd" = "calculator", "file_path" = "main.py", "args" = None},
      #  {"cwd" = "calculator", "file_path" = "main.py", "args" = ["3 + 5"]},]
    
    test_cases = [
        {"cwd" : "calculator", "file_path" :"main.py", "args" : None},
        {"cwd" : "calculator", "file_path" : "main.py", "args" : ["3 + 5"]},
        {"cwd" : "calculator", "file_path" : "tests.py", "args" : None},
        {"cwd" : "calculator", "file_path" : "../main.py", "args" : None},
        {"cwd" : "calculator", "file_path" : "nonexistent.py", "args" : None},
        {"cwd" : "calculator", "file_path" : "lorem.txt", "args" : None}
    ]

    test_nr = 1
    for test in test_cases:
        print(test_nr)
        test_nr += 1
        print(run_python_file(test["cwd"], test["file_path"], test["args"]))


main()