"""A module that offers the "simulation" of the robot"""
from flaskr.robot_movement.robot import Robot

class TestRobot(Robot):
    """
    This class is only for test ticks, because you don't always have the Raspberry Pi available when developing. 
    The movement will simply output
    """

    def _move(self, value:int, axis:str, direction:int) -> None:
        if axis == "Y": #switch direction, because hardware
            if direction:
                direction = False
            else:
                direction = True

        if direction:
            print(f"[DEBUG Move {value} on the {axis}-axis")
        else:
            print(f"[DEBUG] Move {value*-1} on the {axis}-axis")

        self.inform_about_move()


    def reset_pos(self) -> None:
        self._x = -800
        self._y = -800
        self._z = -30000

        self._position_manager.x = self._x
        self._position_manager.y = self._y
        self._position_manager.z = self._z

        self._position_manager.save()
        self.inform_about_move()

        print("[DEBUG] Reseting positions...")
