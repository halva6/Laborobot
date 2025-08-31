from compiler.server_error import VariableNoneTyeError, RobotPositionError

class Robot():
    def __init__(self):
        """is intended to simulate the robot with its 3 different axes for test purposes. 
        This class will be changed later and the actual physical robot will be added"""
        self.MAX_X:int = 10000
        self.MIN_X:int = 0

        self.MAX_Y:int = 10000
        self.MIN_Y:int = 0

        self.MAX_Z:int = 10000
        self.MIN_Z:int = 0

        self.__x:int = 0
        self.__y:int = 0
        self.__z:int = 0


    def move_x(self, value:int) -> None:
        if not value == None:
            if self.MIN_X <= self.__x + value <= self.MAX_X:
                self.__x += value
                print(f"Move {value} on X axis, position on x: {self.__x}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None")

    def move_y(self, value:int) -> None:
        if not value == None:
            if self.MIN_Y <= self.__y + value <= self.MAX_Y:
                self.__y += value
                print(f"Move {value} on Y axis, position on y: {self.__y}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None") 

    def move_z(self, value:int) -> None:
        if not value == None:
            if self.MIN_Z <= self.__z + value <= self.MAX_Z:
                self.__z += value
                print(f"Move {value} on Z axis, position on z: {self.__z}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None")

    def get_x(self) -> int:
        return self.__x
    
    def get_y(self) -> int:
        return self.__y
    
    def get_z(self) -> int:
        return self.__z