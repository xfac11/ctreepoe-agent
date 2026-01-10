from functions.get_file_content import get_file_content
print("Result for calculator/ with file lorem.txt:")
result = get_file_content("calculator", "lorem.txt")
error_split = result.split("[")
print(f"Length of the file: {len(result)}")
print(f"Truncation message: {error_split[1]}")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))

