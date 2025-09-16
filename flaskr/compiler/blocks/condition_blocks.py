from compiler.blocks.block import Block
from compiler.context import Context

class IfBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list):
        super().__init__(id, text, variables, children, 2)

    def execute(self, context:Context) -> None:
        execute_bool:bool = self._get_execute_bool(context=context)
        
        if execute_bool:
            self._execute_children(context)          

    def _get_execute_bool(self, context:Context) -> bool:
        execute_bool:bool = False
        match self._text.split()[1]: # the operator is always in the same place from the text, so you can read it statically
            case "==":
                execute_bool = context.get_variable(self._variables[0]).to_int() == context.get_variable(self._variables[1]).to_int()
            case "<=":
                execute_bool = context.get_variable(self._variables[0]).to_int() <= context.get_variable(self._variables[1]).to_int()
            case ">=":
                execute_bool = context.get_variable(self._variables[0]).to_int() >= context.get_variable(self._variables[1]).to_int()
            case "<":
                execute_bool = context.get_variable(self._variables[0]).to_int() < context.get_variable(self._variables[1]).to_int()
            case ">":
                execute_bool = context.get_variable(self._variables[0]).to_int() > context.get_variable(self._variables[1]).to_int()
        return execute_bool
    

class IfElseBlock(IfBlock):
    def __init__(self, id: str, text:str, variables:list[str], children:list, children_else:list) -> None:
        super().__init__(id, text, variables, children, 2)
        self.__children_else = children_else
    
    def execute(self, context:Context) -> None:
        execute_bool:bool = self._get_execute_bool(context=context)
        
        if execute_bool:
            self._execute_children(context)
        else:
            self._children = self.__children_else
            self._execute_children(context);   