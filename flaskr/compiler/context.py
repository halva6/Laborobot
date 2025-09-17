from compiler.blocks.block import *
from compiler.blocks.variables import Variable
from robot_movement.robot import Robot

class Context():
    def __init__(self, blocks:list, variables:list[Variable], robot: Robot, socket_io: SocketIO):
        self.__variables:list[Variable] = variables
        self.__variables = self.__organize_all_variables(blocks, self.__variables)

        self.__robot: Robot = robot

        self.__socket_io = socket_io

        var_names:list = []
        for var in self.__variables:
            var_names.append(var.get_name())
        print(f"[DEBUG] variables: {var_names}")

    def __organize_all_variables(self, blocks: list, variables: list[Variable]) -> list[Variable]:
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
        """Return of the corresponding variable values based on their names. 
        However, the variables 'X', 'Y', or 'Z' correspond to the current positions on the axes"""
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
        return self.__robot
    
    def get_socket_io(self) -> SocketIO:
        return self.__socket_io