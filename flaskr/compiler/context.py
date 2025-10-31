"""A module that provides all the necessary information, such as variables. It essentially gives the context for the blocks."""

from socket import SocketIO
from typing import TYPE_CHECKING
from flaskr.compiler.blocks.variables import Variable
from flaskr.robot_movement.robot import Robot

if TYPE_CHECKING:
    from flaskr.compiler.blocks.block import Block
class Context():
    """
    provides all the necessary information
    """
    def __init__(self, blocks:list, variables:list[Variable], robot: Robot, socket_io: SocketIO):
        self.__variables:list[Variable] = variables
        self.__variables = self.__organize_all_variables(blocks, self.__variables)

        self.__robot: Robot = robot

        self.__socket_io = socket_io

        var_names:list = []
        for var in self.__variables:
            var_names.append(var.get_name())
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
        unique_vars = {var.get_name(): var for var in variables}

        for block in blocks:
            if block.get_children():
                self.__organize_all_variables(block.get_children(), variables)

            for var in block.get_variables_names():
                if isinstance(var, Variable):
                    unique_vars[var.get_name()] = var

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
            if var.get_name() == name:
                match name:
                    case "X":
                        return Variable("X", self.__robot.get_x())
                    case "Y":
                        return Variable("Y", self.__robot.get_y())
                    case "Z":
                        return Variable("Z", self.__robot.get_z())
                return var

    def get_robot(self) -> Robot:
        """
        returns:
            Robot: the robot object
        """
        return self.__robot

    def get_socket_io(self) -> SocketIO:
        """
        returns:
            SocketIO: the socket io object
        """
        return self.__socket_io
