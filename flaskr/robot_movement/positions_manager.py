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

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        self.__x = value
    
    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = value

    @property
    def z(self) -> int:
        return self.__z

    @z.setter
    def z(self, value: int):
        self.__z = value
