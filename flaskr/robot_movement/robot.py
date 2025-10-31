from server_error import VariableNoneTyeError, RobotPositionError
from robot_movement.positions_manager import PositionManager
from flask_socketio import SocketIO, emit

try:
    from robot_movement.motor_controller import MotorController
except (ImportError, RuntimeError):
    print("[DEBUG] No RPi available")


class Robot():
    def __init__(self, gpio_avialable:bool, socket_io: SocketIO, position_file_path:str):
        """Interface between reading the JSON file coming from the server and executing the real movements of the motor"""

        if gpio_avialable:
            self.__controller = MotorController()
        
        self._position_manager = PositionManager(position_file_path)
        self._position_manager.load()

        self.MAX_X:int = 0
        self.MIN_X:int = -80000

        self.MAX_Y:int = 0
        self.MIN_Y:int = -800000

        self.MAX_Z:int = 0
        self.MIN_Z:int = -100000

        self._x:int = self._position_manager.get_x()
        self._y:int = self._position_manager.get_y()
        self._z:int = self._position_manager.get_z()

        self._axis_lst:list = ["X","Y","Z"]

        self._socket_io:SocketIO = socket_io

        #self.__steps_per_click = 500

        print(f"[DEBUG] init pos -> X: {self._x}, Y: {self._y}, Z: {self._z}")

    def move_x(self, value:int) -> None:
        if not value == None:
            if self.MIN_X <= self._x + value <= self.MAX_X:

                self._x += value
                self._position_manager.set_x(self._x)
                self._position_manager.save()

                if value < 0:
                    self._move(value * -1, "X", False)
                else:
                    self._move(value, "X", True)

                print(f"[DEBUG] Move {value} on X axis, position on x: {self._x}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None")

    def move_y(self, value:int) -> None:
        if not value == None:
            if self.MIN_Y <= self._y + value <= self.MAX_Y:
                
                self._y += value
                self._position_manager.set_y(self._y)
                self._position_manager.save()

                if value < 0:
                    self._move(value * -1, "Y", False)
                else:
                    self._move(value, "Y", True)

                print(f"[DEBUG] Move {value} on Y axis, position on y: {self._y}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None") 

    def move_z(self, value:int) -> None:
        if not value == None:
            if self.MIN_Z <= self._z + value <= self.MAX_Z:

                self._z += value
                self._position_manager.set_z(self._z)
                self._position_manager.save()

                if value < 0:
                    self._move(value * -1, "Z", False)
                else:
                    self._move(value, "Z", True)
                
                print(f"[DEBUG] Move {value} on Z axis, position on z: {self._z}")
            else:
                raise RobotPositionError(f"the value exceeds the limits of the possible movement of the robot")
        else:
            raise VariableNoneTyeError("Variable is no defined, its None")
    
    def move_to_position(self, p_x:int, p_y:int, p_z:int):
        self.move_x(p_x-(self._x))
        self.move_y(p_y-(self._y))
        self.move_z(p_z-(self._z))

    def _move(self, value:int, axis:str, direction:bool) -> None:
        direction = self.__controller.DIR_TO_ENDSTOP if direction else self.__controller.DIR_BACK
        self.__controller.step_motor(steps=value, axis=axis, direction=direction)
        self.inform_about_move()

    def inform_about_move(self) -> None:
        self._socket_io.emit('coords', {'data': f'X: {self._x}, Y: {self._y}, Z: {self._z} '})

        
    def reset_pos(self) -> None:
        for axis in self._axis_lst:
            self.__controller.drive_all_to_endstops(axis)

        pos_dict:dict = self.__controller.get_positions()
        self._x = pos_dict["X"]
        self._y = pos_dict["Y"]
        self._z = pos_dict["Z"]

        self._position_manager.set_x(self._x)
        self._position_manager.set_y(self._y)
        self._position_manager.set_z(self._z)

        self._position_manager.save()

        print("[DEBUG] Reseting positions...") 

    def get_x(self) -> int:
        return self._x
    
    def get_y(self) -> int:
        return self._y
    
    def get_z(self) -> int:
        return self._z