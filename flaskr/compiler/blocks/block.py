from flask_socketio import SocketIO

from compiler.blocks.variables import Variable
from compiler.context import Context

from server_error import ExpectVariableError


class Block:
    """ Functions and variables that start 
    with _ are protected and functions and variables 
    with __ are private, 
    the rest is public """

    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list):
        """ Block class is the parent class of each block 
        and provides the corresponding functionalities """
        self._id: str = id
        self._type: str  = type
        self._text: str = text
        self._variables: list[str] = variables
        self._children: list = children

        if not len(variables) == self._expected_variables:
            raise ExpectVariableError("Expected variables but got none", block_id=self._id)

    def execute(self, context: Context) -> None:
        raise NotImplementedError

    def _execute_children(self, context:Context) -> None:
        for child in self._children:
            child.execute(context)
        
    def get_variables_names(self) -> list[str]:
        return self._variables
    
    def get_children(self) -> list:
        return self._children

    def get_id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return str(self._id)

class MoveBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list) -> None:
        self._expected_variables = 1 # define the exact number of expected variables
        super().__init__(id, type, text, variables, children)
    
    def execute(self, context:Context) -> None:
        if self._id.startswith("block-steps-x"):
            # since it is specified in advance that each block has an exact number of expected variables, 
            # one can therefore directly access the respective variable from the list
            x = context.get_variable(self._variables[0]).to_int() 
            context.get_robot().move_x(x)
        
        if self._id.startswith("block-steps-y"):
            y = context.get_variable(self._variables[0]).to_int()
            context.get_robot().move_y(y)

        if self._id.startswith("block-steps-z"):
            z = context.get_variable(self._variables[0]).to_int()
            context.get_robot().move_z(z)

class ResetPositionBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list):
        self._expected_variables = 0
        super().__init__(id, type, text, variables, children)
    
    def execute(self, context:Context) -> None: #only for test purpose
        context.get_robot().reset_pos()


class IfBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list):
        self._expected_variables = 2
        super().__init__(id, type, text, variables, children)

    def execute(self, context:Context):
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
    def __init__(self, id: str, type:str, text:str, variables:list[str], children:list, children_else:list) -> None:
        self._expected_variables = 4
        super().__init__(id, type, text, variables, children)
        self.__children_else = children_else
    
    def execute(self, context:Context) -> None:
        execute_bool:bool = self._get_execute_bool(context=context)
        
        if execute_bool:
            self._execute_children(context)
        else:
            self._children = self.__children_else
            self._execute_children(context);   

class RepeatBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list) -> None:
        self._expected_variables = 1
        super().__init__(id, type, text, variables, children)
        self.__break_child = self.__find_break_child(children=children)
        self.__break: bool = False
    
    def execute(self, context: Context) -> None:
        for _ in range(context.get_variable(self._variables[0]).to_int()):
            self._execute_children(context)
            if self.__break:
                break

    def _execute_children(self, context) -> None:
        for child in self._children:
            child.execute(context)
            if not self.__break_child == None: # checks if the BreakBlock has been executed
                if self.__break_child.is_active():
                    self.__break = True # if so, this informs the actual loop, in execute() that it should be interrupted immediately
                    break

    def __find_break_child(self, children:list):
        """recursively searches if there is a BreakBlock at all"""
        for child in children:
            if not child.get_children() == []:
                return self.__find_break_child(child.get_children())
            
            if "break" in child.get_id():
                return child
        return None
    
class BreakBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list) -> None:
        """breaks the loop immediately
        If you encounter it during execution, it becomes active, so to speak. 
        The loop checks at each step whether it has been interrupted, 
        i.e. whether the BreakBlock is active, if so, then the loop is interrupted"""
        self._expected_variables = 0
        super().__init__(id, type, text, variables, children)
        self.__active: bool = False

    def execute(self, context:Context) -> None:
        self.__active = True

    def is_active(self) -> bool:
        return self.__active

class DebugPrintBlock(Block):
    def __init__(self, id:str, type:str, text:str, variables:list[str], children:list, socket_io:SocketIO) -> None:
        self._expected_variables = 1
        super().__init__(id, type, text, variables, children)
        self._socket_io:SocketIO = socket_io
    
    def execute(self, context) -> None:
        """sends data to the frontend, which is to be output in the console there, with the corresponding variable values"""
        if not self._variables == []:
            self._socket_io.emit('update', {'data': f'[DEBUG] {context.get_variable(self._variables[0]).get_value()}'})
            print(f'[DEBUG] {context.get_variable(self._variables[0]).get_value()}')
