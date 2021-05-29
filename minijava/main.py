from MinijavaParser import Parser
from Visitors import AstPrinter

with open("./samples/trash.java") as file:
    data='\n'.join(file.readlines())

ast = Parser(data).get_ast()

printer = AstPrinter(ast)
printer.print()