"""A module that offers measurements with measuring devices via GoDirect, allowing experiments to be conducted with the robot"""

import os
import logging
from godirect import GoDirect
from scipy.io import savemat
import numpy as np

from flaskr.server_error import DiviceNotFoundError, NoDeviceConnected

class GoDirectDataCollector:
    """
    it collects the measurement data and stores it in a Matlab-compatible format
    """
    def __init__(self, device_threshold:int=-100, num_measurements:int=50, period:int=100, save_to_desktop:bool=True) -> None:
        """
        args:
            device_threshold (int): Signal threshold for detecting GoDirect devices
            num_measurements (int): Number of measurements to collect
            period (int): Period between each measurement in milliseconds
            save_to_desktop (bool): Boolean flag to determine if the data should be saved on the Desktop
        """
        self.device_threshold:int = device_threshold
        self.num_measurements:int = num_measurements
        self.period:int = period
        self.save_to_desktop:bool = save_to_desktop

        self.godirect:GoDirect = GoDirect(use_ble=True, use_usb=True)
        self.device = None
        self.sensors:list = []
        self.sensor_names:list = []
        self.indices:list = []
        self.values:list = []

        # Initialize logging (optional)
        logging.basicConfig()

    def connect_to_device(self) -> None:
        """Search and connect to a GoDirect device."""
        print("[MEASURMENT] Searching...", flush=True, end="")
        self.device = self.godirect.get_device(threshold=self.device_threshold)

        if self.device is not None and self.device.open(auto_start=False):
            print("\n[MEASURMENT] Connecting...")
            print("[MEASURMENT] Connected to " + self.device.name)
            return True
        else:
            raise DiviceNotFoundError("No GoDirect device found or connection failed")

    def start_reading(self) -> None:
        """Start the data collection from the device."""
        if self.device:
            self.device.start(period=self.period)
            print("[MEASURMENT] Start reading...\n")

            # Get list of enabled sensors and their names
            self.sensors = self.device.get_enabled_sensors()
            self.sensor_names = [s.sensor_description for s in self.sensors]
        else:
            raise NoDeviceConnected("No device connected to start reading")

    def collect_data(self) -> None:
        """Collect measurements from the connected device."""
        for i in range(1, self.num_measurements + 1):
            if self.device.read():  # If data is available
                for sensor in self.sensors:
                    val = sensor.values
                    if val:  # Only store data if a valid value exists
                        print(f"{i}: {sensor.sensor_description} -> {val}")
                        self.indices.append(i)
                        self.values.append(val[0])  # Store first value if it's a single value
                    sensor.clear()  # Clear the sensor data buffer

    def stop_device(self) -> None:
        """Stop the data collection and disconnect the device."""
        if self.device:
            self.device.stop()
            self.device.close()

    def save_data(self) -> None:
        """Save collected data to a .mat file in MATLAB format."""
        if self.save_to_desktop:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            mat_file = os.path.join(desktop_path, "GoDirect_Messdaten.mat")

            # Prepare data to be saved
            data_dict = {
                'index': np.array(self.indices),
                'values': np.array(self.values),
                'sensor_names': np.array(self.sensor_names, dtype=object)  # Store sensor names as object (strings)
            }

            # Save to .mat file (MATLAB format)
            savemat(mat_file, data_dict, do_compression=True)
            print(f"\n[MEASURMENT] Data successfully saved to:\n{mat_file}")
        else:
            print("[DEBUG] nothing saved, can save only on the desktop")

    def quit(self) -> None:
        """Quit and clean up the GoDirect connection."""
        self.godirect.quit()

    def run(self) -> None:
        """Run the complete data collection process."""
        if self.connect_to_device():
            self.start_reading()
            self.collect_data()
            self.stop_device()
            self.save_data()
            self.quit()
