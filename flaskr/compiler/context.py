"""A module that provides all the necessary information, such as variables. It essentially gives the context for the blocks."""

from socket import SocketIO
from typing import TYPE_CHECKING
from flaskr.compiler.blocks.variables import Variable
from flaskr.robot_movement.robot import Robot
from flaskr.measurement import GoDirectDataCollector

if TYPE_CHECKING:
    from flaskr.compiler.blocks.block import Block
class Context():
    """
    provides all the necessary information
    """
    def __init__(self, blocks:list, variables:list[Variable], robot: Robot, go_direct_data_collector: GoDirectDataCollector, socket_io: SocketIO):
        self.__variables:list[Variable] = variables
        self.__variables = self.__organize_all_variables(blocks, self.__variables)

        self.__go_direct_data_collector: GoDirectDataCollector = go_direct_data_collector
        self.__robot: Robot = robot

        self.__socket_io = socket_io

        var_names:list = []
        for var in self.__variables:
            var_names.append(var.name)
        print(f"[DEBUG] variables: {var_names}")

    def __organize_all_variables(self, blocks: list["Block"], variables: list[Variable]) -> list[Variable]:
        """
        organizes variables from blocks and ensures unique variable names
        args:
            blocks (list[Block]): list of blocks to extract variables from
            variables (list[Variable]): list of existing variables to update
        returns:
            list[Variable]: updated list of unique variables
        """
        # Create a dictionary to ensure unique variable names
        unique_vars = {var.name: var for var in variables}

        for block in blocks:
            if block.children:
                self.__organize_all_variables(block.children, variables)

            for var in block.variables_names:
                if isinstance(var, Variable):
                    unique_vars[var.name] = var

        # Update the original list in-place
        variables.clear()
        variables.extend(unique_vars.values())
        return variables

    def get_variable(self, name:str) -> Variable:
        """
        Return of the corresponding variable values based on their names. 
        However, the variables 'X', 'Y', or 'Z' correspond to the current positions on the axes
        args:
            name (str): the name of the variable to retrieve
        returns:
            Variable: the variable object corresponding to the given name
        """
        for var in self.__variables:
            if var.name == name:
                match name:
                    case "X":
                        return Variable("X", self.__robot.x)
                    case "Y":
                        return Variable("Y", self.__robot.y)
                    case "Z":
                        return Variable("Z", self.__robot.z)
                return var

    @property
    def robot(self) -> Robot:
        return self.__robot
    
    @property
    def socket_io(self) -> SocketIO:
        return self.__socket_io
    
    @property
    def go_direct_data_collector(self) -> GoDirectDataCollector:
        return self.__go_direct_data_collector
