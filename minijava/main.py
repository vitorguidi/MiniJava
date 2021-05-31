from MinijavaParser import Parser
from Visitors import AstPrinter

with open("./samples/smallTest.java") as file:
    data='\n'.join(file.readlines())

ast = Parser(data).get_ast()

printer = AstPrinter(ast)
printer.print()