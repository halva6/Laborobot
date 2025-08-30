from compiler.Blocks.block import *
from compiler.Blocks.variables import Variable
from compiler.robot import Robot

class Context():
    def __init__(self, blocks, robot):
        self.__variables:list[Variable] = []
        self.__variables:list[Variable] = self.__get_all_variables(blocks, self.__variables)

        self.__robot = robot

        var_names = []
        for var in self.__variables:
            var_names.append(var.get_name())
        print(f"[DEBUG] variables: {var_names}")

    def __get_all_variables(self, blocks:list, variables:list[Variable]) -> list[Variable]:
        for block in blocks:
            if not block.get_children() == []:
                self.__get_all_variables(block.get_children(), variables)

            for var in block.get_variables():
                found: bool = True
                for var2 in variables:
                    if var.get_name() == var2.get_name() and found:
                        found = False
                if found:
                    variables.append(var)
        return variables
    
    def get_variable(self, name):
        for var in self.__variables:
            if var.get_name() == name:
                match name:
                    case "X":
                        return self.__robot.get_x()
                    case "Y":
                        return self.__robot.get_y()
                    case "Z":
                        return self.__robot.get_z()
                return var.get_value()
            