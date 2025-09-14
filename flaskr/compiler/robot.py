from compiler.server_error import VariableNoneTyeError, RobotPositionError
from compiler.positions_manager import PositionManager
from compiler.motor_controller import MotorController


class Robot():
    def __init__(self):
        """is intended to simulate the robot with its 3 different axes for test purposes. 
        This class will be changed later and the actual physical robot will be added"""

        self.__controller = MotorController()
        self.__position_manager = PositionManager("flaskr/compiler/position.json")
        self.__position_manager.load()

        self.MAX_X:int = 0
        self.MIN_X:int = -80000

        self.MAX_Y:int = 0
        self.MIN_Y:int = -800000

        self.MAX_Z:int = 0
        self.MIN_Z:int = -100000

        self.__x:int = self.__position_manager.get_x()
        self.__y:int = self.__position_manager.get_y()
        self.__z:int = self.__position_manager.get_z()

        self.__axis_lst:list = ["X","Y","Z"]

        #self.__steps_per_click = 500

        print(f"X: {self.__x}, Y: {self.__y}, Z: {self.__z}")

    def move_x(self, value:int) -> None:
        if not value == None:
            if self.MIN_X <= self.__x + value <= self.MAX_X:
                if value < 0:
                    self.__move(value * -1, "X", False)
                else:
                    self.__move(value, "X", True)

                self.__x += value
                self.__position_manager.set_x(self.__x)
                self.__position_manager.save()
                print(f"Move {value} on X axis, position on x: {self.__x}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None")

    def move_y(self, value:int) -> None:
        if not value == None:
            if self.MIN_Y <= self.__y + value <= self.MAX_Y:
                if value < 0:
                    self.__move(value * -1, "Y", False)
                else:
                    self.__move(value, "Y", True)
                
                self.__y += value
                self.__position_manager.set_y(self.__y)
                self.__position_manager.save()
                print(f"Move {value} on Y axis, position on y: {self.__y}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None") 

    def move_z(self, value:int) -> None:
        print(value)
        if not value == None:
            if self.MIN_Z <= self.__z + value <= self.MAX_Z:

                if value < 0:
                    self.__move(value * -1, "Z", False)
                else:
                    self.__move(value, "Z", True)

                self.__z += value
                self.__position_manager.set_z(self.__z)
                self.__position_manager.save()
                print(f"Move {value} on Z axis, position on z: {self.__z}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None")
        
    def __move(self, value, axis, positive):
        direction = self.__controller.DIR_TO_ENDSTOP if positive else self.__controller.DIR_BACK
        self.__controller.step_motor(axis=axis, steps=value, direction=direction)
        
    def reset_pos(self) -> None:
        for axis in self.__axis_lst:
            self.__controller.drive_all_to_endstops(axis)

        pos_dict:dict = self.__controller.get_positions()
        print(pos_dict)
        self.__x = pos_dict["X"]
        self.__y = pos_dict["Y"]
        self.__z = pos_dict["Z"]

        self.__position_manager.set_x(self.__x)
        self.__position_manager.set_y(self.__y)
        self.__position_manager.set_z(self.__z)

        self.__position_manager.save()

        print("Reseting...") 

    def get_x(self) -> int:
        return self.__x
    
    def get_y(self) -> int:
        return self.__y
    
    def get_z(self) -> int:
        return self.__z