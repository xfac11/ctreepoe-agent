from functions.write_file import write_file

def main():
    print("Ressult of writing to working dir calculator and file path lorem.txt:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("Ressult of writing to working dir calculator and file path pkg/morelorem.txt:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("Ressult of writing to working dir calculator and file path /tmp/temp.txt:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

main()