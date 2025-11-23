"""A module that offers measurements with measuring devices via GoDirect, allowing experiments to be conducted with the robot"""

import os
import logging
from godirect import GoDirect, GoDirectDevice
from scipy.io import savemat
import numpy as np

from flaskr.server_error import DiviceNotFoundError, NoDeviceConnected

class GoDirectDataCollector:
    """
    it collects the measurement data and stores it in a Matlab-compatible format
    """
    def __init__(self, device_threshold:int=-100, num_measurements:int=1, period:int=100, save_to_desktop:bool=True) -> None:
        """
        args:
            device_threshold (int): Signal threshold for detecting GoDirect devices
            num_measurements (int): Number of measurements to collect
            period (int): Period between each measurement in milliseconds
            save_to_desktop (bool): Boolean flag to determine if the data should be saved on the Desktop
        """
        self.__file_path:str = os.path.join(os.path.expanduser("~"), "Desktop")
        self.__delete_file()

        self.__device_threshold:int = device_threshold
        self.__num_measurements:int = num_measurements
        self.__period:int = period
        self.__save_to_desktop:bool = save_to_desktop

        self.__godirect:GoDirect = GoDirect(use_ble=True, use_usb=True)
        self.__device:GoDirectDevice = None
        self.__sensors:list = []
        self.__sensor_names:list = []
        self.__indices:list = []
        self.__values:list = []

        self.__pos_x:list = []
        self.__pos_y:list = []
        self.__pos_z:list = []


        self.__is_connected:bool = self.connect_to_device()

        # Initialize logging (optional)
        logging.basicConfig()

    def __delete_file(self):
        """
        deletes the file, from an external perspective, writing the file represents the process of replacing the file
        """
        file: str = self.__file_path+"GoDirect_Data.mat"
        if os.path.exists(file):
            os.remove(file)

    def connect_to_device(self) -> None:
        """
        search and connect to a GoDirect device
        """
        print("[MEASURMENT] Searching...", flush=True, end="")
        self.__device = self.__godirect.get_device(threshold=self.__device_threshold)

        if self.__device is not None and self.__device.open(auto_start=False):
            print("\n[MEASURMENT] Connecting...")
            print("[MEASURMENT] Connected to " + self.__device.name)
            return True
        else:
            raise DiviceNotFoundError("No GoDirect device found or connection failed")

    def start_reading(self) -> None:
        """
        start the data collection from the device
        """
        if self.__device:
            self.__device.start(period=self.__period)
            print("[MEASURMENT] Start reading...\n")

            # Get list of enabled sensors and their names
            self.__sensors = self.__device.get_enabled_sensors()
            self.__sensor_names = [s.sensor_description for s in self.__sensors]
        else:
            raise NoDeviceConnected("No device connected to start reading")


    def collect_data(self, positions:tuple) -> None:
        """
        collect measurements from the connected device
        """
        for i in range(1, self.__num_measurements + 1):
            if self.__device.read():  # If data is available

                x,y,z = positions

                for sensor in self.__sensors:
                    val = sensor.values
                    if val:
                        print(f"[MEASUREMENT]{i}: {sensor.sensor_description} -> {val}  @ Pos=({x}, {y}, {z})")
                        self.__indices.append(i)
                        self.__values.append(val[0])
                        self.__pos_x.append(x)
                        self.__pos_y.append(y)
                        self.__pos_z.append(z)
                    sensor.clear()


    def stop_device(self) -> None:
        """
        stop the data collection and disconnect the device
        """
        if self.__device:
            self.__device.stop()
            self.__device.close()

    def save_data(self) -> None:
        """
        save collected data to a .mat file in MATLAB format
        """
        if self.__save_to_desktop:
            mat_file = os.path.join(self.__file_path, "GoDirect_Data.mat")

            data_dict = {
                'index': np.array(self.__indices),
                'values': np.array(self.__values),
                'sensor_names': np.array(self.__sensor_names, dtype=object),

                'X': np.array(self.__pos_x),
                'Y': np.array(self.__pos_y),
                'Z': np.array(self.__pos_z)
            }

            savemat(mat_file, data_dict, do_compression=True)
            print(f"\n[MEASURMENT] Data successfully saved to:\n{mat_file}")
        else:
            print("[DEBUG] nothing saved, can save only on the desktop")


    def quit(self) -> None:
        """
        quit and clean up the GoDirect connection
        """
        self.__godirect.quit()

    def start(self) -> None:
        """starts the data collector
        """
        if self.__is_connected:
            self.start_reading()

    def stop(self) -> None:
        """
        shutdown the data collector
        """
        if self.__is_connected:
            self.stop_device()
            self.save_data()
            self.quit()


    def run(self, positions:tuple) -> None:
        """
        collect the data
        """
        if self.__is_connected:
            self.collect_data(positions)
