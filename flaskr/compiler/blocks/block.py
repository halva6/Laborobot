from flask_socketio import SocketIO
import time

from compiler.context import Context
from server_error import *


class Block:
    """ Functions and variables that start 
    with _ are protected and functions and variables 
    with __ are private, 
    the rest is public """

    def __init__(self, id:str, text:str, variables:list[str], children:list, expected_vars: int):
        """ Block class is the parent class of each block 
        and provides the corresponding functionalities """
        self._id: str = id
        self._text: str = text
        self._variables: list[str] = variables
        self._children: list = children          
        self.__validate_vars(expected_vars)

    def __validate_vars(self, expected_vars: int):
        if not len(self._variables) == expected_vars:
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

class DebugPrintBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(id, text, variables, children, 1)
    
    def execute(self, context: Context) -> None:
        """sends data to the frontend, which is to be output in the console there, with the corresponding variable values"""
        if not self._variables == []:
            context.get_socket_io().emit('update', {'data': f'[DEBUG] {context.get_variable(self._variables[0]).get_value()}'})
            print(f'[DEBUG] {context.get_variable(self._variables[0]).get_value()}')

class TimerBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list, time_multiplier: int) -> None:
        super().__init__(id, text, variables, children, 1)
        self.__time_multiplier = time_multiplier
    
    def execute(self, context: Context):
        time.sleep(context.get_variable(self._variables[0]).to_int() * self.__time_multiplier)
