# /home/admin/Laborroboter/motor_controller.py

import RPi.GPIO as GPIO
import time
import threading



class MotorController:
    def __init__(self):
        
        self.STEP_DELAY = 0.0001875

        self.DIR_TO_ENDSTOP = GPIO.HIGH
        self.DIR_BACK = GPIO.LOW
        self.ENA_LOCKED = GPIO.LOW
        self.ENA_RELEASED = GPIO.HIGH
        
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.positions = {"X": 0, "Y": 0, "Z": 0}

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

    def get_positions(self):
        return self.positions.copy()
    
    def set_positions(self, positions):
        self.positions = positions

    def step_motor(self, axis:str, steps, direction):
        pins = self.motors[axis]
        GPIO.output(pins["ENA"], self.ENA_LOCKED)
        GPIO.output(pins["DIR"], direction)

        for _ in range(steps):
            GPIO.output(pins["PUL"], GPIO.HIGH)
            time.sleep(self.STEP_DELAY)
            GPIO.output(pins["PUL"], GPIO.LOW)
            time.sleep(self.STEP_DELAY)
            
            #Turning back to saved positions might differ in terms of direction depending on the used modele
            if axis == "Y":
                if direction == (self.DIR_BACK if not pins["INVERT_DIR"] else self.DIR_TO_ENDSTOP):
                    self.positions[axis] += 1
                else:
                    self.positions[axis] -= 1
            else:
                if direction == (self.DIR_BACK if not pins["INVERT_DIR"] else self.DIR_TO_ENDSTOP):
                    self.positions[axis] -= 1
                else:
                    self.positions[axis] += 1

        GPIO.output(pins["ENA"], self.ENA_RELEASED)

    def _drive_single_axis(self, axis):
            pins = self.motors[axis]
            GPIO.output(pins["ENA"], self.ENA_LOCKED)
            GPIO.output(pins["DIR"], self.DIR_TO_ENDSTOP if not pins["INVERT_DIR"] else self.DIR_BACK)

            # Fahren bis Endschalter
            while GPIO.input(pins["STOP"]) == GPIO.HIGH:
                GPIO.output(pins["PUL"], GPIO.HIGH)
                time.sleep(self.STEP_DELAY)
                GPIO.output(pins["PUL"], GPIO.LOW)
                time.sleep(self.STEP_DELAY)

            # Referenzpunkt setzen
            self.positions[axis] = 0
            time.sleep(0.2)

            # Ein Stück zurückfahren
            GPIO.output(pins["DIR"], self.DIR_BACK if not pins["INVERT_DIR"] else self.DIR_TO_ENDSTOP)
            steps_back = 30000 if axis == "Z" else 800
            for _ in range(steps_back):
                GPIO.output(pins["PUL"], GPIO.HIGH)
                time.sleep(self.STEP_DELAY)
                GPIO.output(pins["PUL"], GPIO.LOW)
                time.sleep(self.STEP_DELAY)
                self.positions[axis] -= 1

            GPIO.output(pins["ENA"], self.ENA_RELEASED)

    def drive_all_to_endstops(self, axes):
        threads = []
        for axis in axes:
            t = threading.Thread(target=self._drive_single_axis, args=(axis,))
            threads.append(t)
            t.start()

        # Warten, bis alle Threads fertig sind
        for t in threads:
            t.join()

    def move_all_axes_simultaneously(self, target_pos:dict):
        threads = []
        current_pos = self.positions.copy()
        
        print(f"[DEBUG] target_pos: {target_pos}, Type: {type(target_pos)}")

        for axis in ["X", "Y", "Z"]:
            diff = target_pos[axis] - current_pos[axis]
            if diff == 0:
                continue
            
            if diff > 0:
                direction = self.DIR_TO_ENDSTOP
            else:
                direction = self.DIR_BACK
                
            #direction = self.DIR_TO_ENDSTOP if diff > 0 else self.DIR_BACK
            steps = abs(diff)
            t = threading.Thread(target=self.step_motor, args=(axis, steps, direction))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def cleanup(self):
        GPIO.cleanup()
