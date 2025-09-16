# /home/admin/Laborroboter/positions_manager.py
import os
import json
from pathlib import Path

class PositionManager:
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

    # Getters and Setters for x, y, z
    def set_x(self, value: float):
        self.__x = value

    def get_x(self) -> float:
        return self.__x

    def set_y(self, value: float):
        self.__y = value

    def get_y(self) -> float:
        return self.__y

    def set_z(self, value: float):
        self.__z = value

    def get_z(self) -> float:
        return self.__z


