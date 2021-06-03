from MinijavaParser import Parser
from Visitors import AstPrinter, CFGPrinter
from CFG import *

with open("./samples/binSearch.java") as file:
    data='\n'.join(file.readlines())

ast = Parser(data).get_ast()

astprinter = AstPrinter(ast)
astprinter.print()

cfg = CFG(ast)
cfg_printer = CFGPrinter(cfg)
cfg_printer.print()