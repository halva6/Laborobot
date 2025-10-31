"""Module that provides control of the motors"""
from typing import Literal
import time
import threading
import RPi.GPIO as GPIO

class MotorController:
    """
    it controls the individual motors and is the last step before it affects the hardware
    """

    #TODO See how it is with these variables, because they are defined twice
    DIR_TO_ENDSTOP: Literal[1] = GPIO.HIGH
    DIR_BACK: Literal[0] = GPIO.LOW

    STEP_DELAY:float = 0.0001875

    def __init__(self):
        #TODO Encapsulate and type all variable types
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.positions:dict = {"X": 0, "Y": 0, "Z": 0}

        self.motors = {
            "X": {"ENA": 22, "PUL": 16, "DIR": 18, "STOP": 11, "INVERT_DIR": False},
            "Y": {"ENA": 33, "PUL": 32, "DIR": 31, "STOP": 13, "INVERT_DIR": True},
            "Z": {"ENA": 37, "PUL": 36, "DIR": 35, "STOP": 15, "INVERT_DIR": False},
        }

        for pins in self.motors.values():
            GPIO.setup(pins["DIR"], GPIO.OUT)
            GPIO.setup(pins["PUL"], GPIO.OUT)
            GPIO.setup(pins["ENA"], GPIO.OUT)
            GPIO.setup(pins["STOP"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def positions(self) -> dict:
        return self.positions.copy()

    def step_motor(self, steps:int, axis:str, direction:bool):
        """
        moves the motor a given number of steps along the specified axis and updates its position
        args:
            steps (int): number of steps to move the motor
            axis (str): axis identifier (e.g. 'x', 'y', 'z')
            direction (bool): direction of movement
        """
        pins = self.motors[axis]
        GPIO.output(pins["ENA"], MotorController.DIR_BACK)
        GPIO.output(pins["DIR"], direction)

        for _ in range(steps):
            GPIO.output(pins["PUL"], MotorController.DIR_TO_ENDSTOP)
            time.sleep(self.STEP_DELAY)
            GPIO.output(pins["PUL"], MotorController.DIR_BACK)
            time.sleep(self.STEP_DELAY)

            #Turning back to saved positions might differ in terms of direction depending on the used modele
            if axis == "Y":
                if direction == (self.DIR_BACK if not pins["INVERT_DIR"] else MotorController.DIR_TO_ENDSTOP):
                    self.positions[axis] += 1
                else:
                    self.positions[axis] -= 1
            else:
                if direction == (self.DIR_BACK if not pins["INVERT_DIR"] else MotorController.DIR_TO_ENDSTOP):
                    self.positions[axis] -= 1
                else:
                    self.positions[axis] += 1

        GPIO.output(pins["ENA"], MotorController.DIR_TO_ENDSTOP)

    def _drive_single_axis(self, axis:str):
        """
        drives a single motor axis to its endstop, sets it as reference, and moves it back slightly
        args:
            axis (str): axis identifier to drive (e.g. 'x', 'y', 'z')
        """
        pins = self.motors[axis]
        GPIO.output(pins["ENA"], MotorController.DIR_BACK)
        GPIO.output(pins["DIR"], MotorController.DIR_TO_ENDSTOP if not pins["INVERT_DIR"] else self.DIR_BACK)

        # Drive until limit switch
        while GPIO.input(pins["STOP"]) == MotorController.DIR_TO_ENDSTOP:
            GPIO.output(pins["PUL"], MotorController.DIR_TO_ENDSTOP)
            time.sleep(self.STEP_DELAY)
            GPIO.output(pins["PUL"], MotorController.DIR_BACK)
            time.sleep(self.STEP_DELAY)

        # Set reference point
        self.positions[axis] = 0
        time.sleep(0.2)

        # Drive back a bit
        GPIO.output(pins["DIR"], self.DIR_BACK if not pins["INVERT_DIR"] else MotorController.DIR_TO_ENDSTOP)
        steps_back = 30000 if axis == "Z" else 800
        for _ in range(steps_back):
            GPIO.output(pins["PUL"], MotorController.DIR_TO_ENDSTOP)
            time.sleep(self.STEP_DELAY)
            GPIO.output(pins["PUL"], MotorController.DIR_BACK)
            time.sleep(self.STEP_DELAY)
            self.positions[axis] -= 1

        GPIO.output(pins["ENA"], MotorController.DIR_TO_ENDSTOP)

    def drive_all_to_endstops(self, axes):
        """
        drives all specified motor axes to their endstops using parallel threads
        args:
            axes (list): list of axis identifiers to drive (e.g. ['x', 'y', 'z'])
        """
        threads = []
        for axis in axes:
            t = threading.Thread(target=self._drive_single_axis, args=(axis,))
            threads.append(t)
            t.start()

        # wait until all threads are finished.
        for t in threads:
            t.join()

    def move_all_axes_simultaneously(self, target_pos:dict):
        """
        moves all motor axes simultaneously to their target positions using threading
        args:
            target_pos (dict): dictionary containing target positions for each axis
        """
        #TODO real parallel movement of the motors, but it could also be that this is a hardware problem
        threads = []
        current_pos = self.positions.copy()

        print(f"[DEBUG] target_pos: {target_pos}, Type: {type(target_pos)}")

        for axis in ["X", "Y", "Z"]:
            diff = target_pos[axis] - current_pos[axis]
            if diff == 0:
                continue

            if diff > 0:
                direction = MotorController.DIR_TO_ENDSTOP
            else:
                direction = self.DIR_BACK

            #direction = MotorController.DIR_TO_ENDSTOP if diff > 0 else self.DIR_BACK
            steps = abs(diff)
            t = threading.Thread(target=self.step_motor, args=(axis, steps, direction))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def cleanup(self):
        """
        cleans up all gpio resources
        """
        GPIO.cleanup()
