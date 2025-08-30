from compiler.Blocks.variables import Variable
from compiler.context import Context
from compiler.robot import Robot

class Block:
    def __init__(self, id:str, type:str, text:str, variables:list[Variable], children:list):
        self._id: str = id
        self._type: str  = type
        self._commands:list[str] = text.split(" ")
        self._variables: list[Variable] = variables
        self._children: list = children


    def _execute(self, context: Context, robot: Robot) -> None:
        raise NotImplementedError()
    
    def _execute_children(self, context:Context, robot: Robot) -> None:
        for child in self._children:
            child._execute(context, robot)
        
    def get_variables(self) -> list[Variable]:
        return self._variables
    
    def get_children(self) -> list:
        return self._children

class MoveBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[Variable], children:list) -> None:
        super().__init__(id, type, text, variables, children)
    
    def _execute(self, context:Context, robot: Robot) -> None:
        if self._id.startswith("block-steps-x"):
            x = context.get_variable(self._commands[1])
            robot.move_x(x)
        
        if self._id.startswith("block-steps-y"):
            y = context.get_variable(self._commands[1])
            robot.move_y(y)

        if self._id.startswith("block-steps-z"):
            z = context.get_variable(self._commands[1])
            robot.move_z(z)

class IfBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[Variable], children:list):
        super().__init__(id, type, text, variables, children)

    def _execute(self, context:Context, robot: Robot):

        execute_bool:bool = self._get_execute_bool(commands=self._commands, context=context)
        
        if execute_bool:
            self._execute_children(context, robot)          

    def _get_execute_bool(self, commands:list, context:Context) -> bool:
        execute_bool:bool = False
        match commands[2]:
            case "==":
                execute_bool = context.get_variable(commands[1]) == context.get_variable(commands[3])
            case "<=":
                execute_bool = context.get_variable(commands[1]) <= context.get_variable(commands[3])
            case ">=":
                execute_bool = context.get_variable(commands[1]) >= context.get_variable(commands[3])
            case "<":
                execute_bool = context.get_variable(commands[1]) < context.get_variable(commands[3])
            case ">":
                execute_bool = context.get_variable(commands[1]) > context.get_variable(commands[3])
        return execute_bool
    

class IfElseBlock(IfBlock):
    def __init__(self, id: str, type:str, text:str, variables:list[Variable], children:list, children_else:list) -> None:
        super().__init__(id, type, text, variables, children)
        self.__children_else = children_else
    
    def _execute(self, context:Context, robot: Robot) -> None:
        execute_bool:bool = self._get_execute_bool(commands=self._commands, context=context)
        
        if execute_bool:
            self._execute_children(context, robot)
        else:
            self._children = self.__children_else
            self._execute_children(context, robot);   

class RepeatBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[Variable], children:list) -> None:
        super().__init__(id, type, text, variables, children)
    
    def _execute(self, context: Context, robot: Robot) -> None:
        for _ in range(context.get_variable(self._commands[1])):
            self._execute_children(context, robot)
    
class EventBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[Variable], children:list) -> None:
        super().__init__(id, type, text, variables, children)
    
    def _execute(self, context:Context, robot: Robot) -> None:
        pass