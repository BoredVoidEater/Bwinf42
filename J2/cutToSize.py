CHAR_LIMIT = 300

with open("Beispiel6.txt", "r",encoding="cp1252") as input_file:
    content = input_file.read()


    with open("Test.txt","w",encoding="utf-8") as file:
        file.write(content[0:CHAR_LIMIT])
        file.write(content[len(content)-CHAR_LIMIT-1:len(content)-1])
    