from MinijavaParser import Parser

with open("./samples/trash.java") as file:
    data='\n'.join(file.readlines())

parser = Parser(data)
