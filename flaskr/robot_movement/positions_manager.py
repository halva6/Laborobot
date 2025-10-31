"""Module that offers permanent storage of positions"""
import json
from pathlib import Path

class PositionManager:
    """
    It saves and manages the positions so that, for example, they are not reset after a restart, 
    because the robot does not automatically reset its motors.
    """
    def __init__(self, filepath: str):
        self.__filepath = Path(filepath)
        self.__x: int = None
        self.__y: int = None
        self.__z: int = None
        self.load()

    def load(self) -> None:
        """Load x, y, z from JSON if the file exists, otherwise use default values."""
        if self.__filepath.exists():
            with open(self.__filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.__x = data.get("X", 0)
                self.__y = data.get("Y", 0)
                self.__z = data.get("Z", 0)
        else:
            print("[ERROR] fail to load positions from file")
            self.__x, self.__y, self.__z = 0, 0, 0

    def save(self) -> None:
        """Save x, y, z into the JSON file."""
        data = {"X": self.__x, "Y": self.__y, "Z": self.__z}
        with open(self.__filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def set_x(self, value: int):
        """
        args:
            value (int): value of x
        """
        self.__x = value

    def get_x(self) -> int:
        """
        returns:
            int: x coordinate
        """
        return self.__x

    def set_y(self, value: int):
        """
        args:
            value (int): value of x
        """
        self.__y = value

    def get_y(self) -> int:
        """
        returns:
            int: y coordinate
        """
        return self.__y

    def set_z(self, value: int):
        """
        args:
            value (int): value of z
        """
        self.__z = value

    def get_z(self) -> int:
        """
        returns:
            int: z coordinate
        """
        return self.__z
