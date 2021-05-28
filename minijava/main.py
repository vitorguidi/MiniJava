import sys

print(sys.path)

from MinijavaParser import Parser

with open("./samples/smallTest.java") as file:
    data='\n'.join(file.readlines())

parser = Parser(data)