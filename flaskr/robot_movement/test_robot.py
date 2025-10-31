from robot_movement.robot import Robot
from flask_socketio import SocketIO, emit

class TestRobot(Robot):
    def __init__(self, gpio_avialable:bool, socket_io: SocketIO, position_file_path:str):
        """This class is only for test ticks, because you don't always have the Raspberry Pi available when developing. 
        The movement will simply output"""
        super().__init__(gpio_avialable, socket_io, position_file_path)


    def _move(self, value:int, axis:str, direction:bool) -> None:
        if direction:
            print(f"[DEBUG Move {value} on the {axis}-axis")
        else:
            print(f"[DEBUG] Move {value*-1} on the {axis}-axis")
        
        self.inform_about_move()

        
    def reset_pos(self) -> None:
        self._x = -800
        self._y = -800
        self._z = -30000

        self._position_manager.set_x(self._x)
        self._position_manager.set_y(self._y)
        self._position_manager.set_z(self._z)

        self._position_manager.save()
        self.inform_about_move()

        print("[DEBUG] Reseting positions...") 
