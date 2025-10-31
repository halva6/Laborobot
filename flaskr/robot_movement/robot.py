"""Module that provides control of the robot"""

from flask_socketio import SocketIO
from flaskr.server_error import VariableNoneTyeError, RobotPositionError
from flaskr.robot_movement.positions_manager import PositionManager

try:
    from robot_movement.motor_controller import MotorController
except (ImportError, RuntimeError):
    print("[DEBUG] No RPi available")


class Robot():
    """
    Interface between reading the JSON file coming from the server and executing the real movements of the motor
    """
    MAX_X:int = 0
    MIN_X:int = -80000

    MAX_Y:int = 0
    MIN_Y:int = -800000

    MAX_Z:int = 0
    MIN_Z:int = -100000

    def __init__(self, gpio_avialable:bool, socket_io: SocketIO, position_file_path:str):
        if gpio_avialable:
            self.__controller = MotorController()

        self._position_manager = PositionManager(position_file_path)
        self._position_manager.load()

        self._x:int = self._position_manager.x
        self._y:int = self._position_manager.y
        self._z:int = self._position_manager.z

        self._axis_lst:list = ["X","Y","Z"]

        self._socket_io:SocketIO = socket_io

        #self.__steps_per_click = 500

        print(f"[DEBUG] init pos -> X: {self._x}, Y: {self._y}, Z: {self._z}")

    def move_on_axis(self, axis: str, value: int) -> None:
        """
        Moves the robot along the given axis ('X', 'Y' or 'Z') by the given value if within limits.
        Args:
            axis (str): Axis to move along ('X', 'Y', or 'Z')
            value (int): Distance to move along the axis
        """
        if value is None:
            raise VariableNoneTyeError("Variable is not defined, it's None")

        axis = axis.upper()

        # Mapping for each axis to its attribute and limits
        axis_map = {
            "X": ("_x", "MIN_X", "MAX_X"),
            "Y": ("_y", "MIN_Y", "MAX_Y"),
            "Z": ("_z", "MIN_Z", "MAX_Z"),
        }

        if axis not in axis_map:
            raise ValueError("Axis must be one of 'X', 'Y', or 'Z'")

        attr_name, min_attr, max_attr = axis_map[axis]

        # Get current position and limits dynamically
        current_value = getattr(self, attr_name)
        min_limit = getattr(Robot, min_attr)
        max_limit = getattr(Robot, max_attr)

        if not min_limit <= current_value + value <= max_limit:
            raise RobotPositionError("The value exceeds the limits of the possible movement of the robot")

        new_value = current_value + value
        setattr(self, attr_name, new_value)

        setattr(self._position_manager, axis.lower(), new_value)
        self._position_manager.save()

        self._move(abs(value), axis, value >= 0)

        print(f"[DEBUG] Move {value} on {axis} axis, position on {axis.lower()}: {new_value}")


    def move_to_position(self, p_x:int, p_y:int, p_z:int):
        """
        moves the robot to the specified x y and z coordinates
        args:
            p_x (int): target x coordinate
            p_y (int): target y coordinate
            p_z (int): target z coordinate
        """
        self.move_on_axis("X", p_x-(self._x))
        self.move_on_axis("Y", p_y-(self._y))
        self.move_on_axis("Z", p_z-(self._z))

    def _move(self, value:int, axis:str, direction:bool) -> None:
        """
        moves the specified axis by a given value in a given direction
        args:
            value (int): number of steps to move
            axis (str): axis identifier (e.g. 'x', 'y', 'z')
            direction (bool): movement direction
        """
        direction = self.__controller.DIR_TO_ENDSTOP if direction else self.__controller.DIR_BACK
        self.__controller.step_motor(steps=value, axis=axis, direction=direction)
        self.inform_about_move()

    def inform_about_move(self) -> None:
        """
        emits the current robot coordinates via socket io
        """
        self._socket_io.emit('coords', {'data': f'X: {self._x}, Y: {self._y}, Z: {self._z} '})


    def reset_pos(self) -> None:
        """
        resets all axes to their endstops and updates stored positions
        """
        for axis in self._axis_lst:
            self.__controller.drive_all_to_endstops(axis)

        pos_dict:dict = self.__controller.positions
        self._x = pos_dict["X"]
        self._y = pos_dict["Y"]
        self._z = pos_dict["Z"]

        self._position_manager.x = self._x
        self._position_manager.y = self._y
        self._position_manager.z = self._z

        self._position_manager.save()

        print("[DEBUG] Reseting positions...")

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def z(self) -> int:
        return self._z
