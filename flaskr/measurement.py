from godirect import GoDirect
from scipy.io import savemat
import numpy as np
import os
import logging

from server_error import DisabledSavingError, DiviceNotFoundError, NoDeviceConnected

class GoDirectDataCollector:
    def __init__(self, device_threshold=-100, num_measurements=50, period=100, save_to_desktop=True):
        """
        Initialize the GoDirectDataCollector object.
        
        :param device_threshold: Signal threshold for detecting GoDirect devices (default -100).
        :param num_measurements: Number of measurements to collect (default 50).
        :param period: Period between each measurement in milliseconds (default 100ms).
        :param save_to_desktop: Boolean flag to determine if the data should be saved on the Desktop (default True).
        """
        self.device_threshold = device_threshold
        self.num_measurements = num_measurements
        self.period = period
        self.save_to_desktop = save_to_desktop
        
        self.godirect = GoDirect(use_ble=True, use_usb=True)
        self.device = None
        self.sensors = []
        self.sensor_names = []
        self.indices = []
        self.values = []
        
        # Initialize logging (optional)
        logging.basicConfig()

    def connect_to_device(self):
        """Search and connect to a GoDirect device."""
        print("[MEASURMENT] Searching...", flush=True, end="")
        self.device = self.godirect.get_device(threshold=self.device_threshold)

        if self.device is not None and self.device.open(auto_start=False):
            print("\n[MEASURMENT] Connecting...")
            print("[MEASURMENT] Connected to " + self.device.name)
            return True
        else:
            raise DiviceNotFoundError("No GoDirect device found or connection failed")

    def start_reading(self):
        """Start the data collection from the device."""
        if self.device:
            self.device.start(period=self.period)
            print("[MEASURMENT] Start reading...\n")
            
            # Get list of enabled sensors and their names
            self.sensors = self.device.get_enabled_sensors()
            self.sensor_names = [s.sensor_description for s in self.sensors]
        else:
            raise NoDeviceConnected("No device connected to start reading")
    
    def collect_data(self):
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

    def stop_device(self):
        """Stop the data collection and disconnect the device."""
        if self.device:
            self.device.stop()
            self.device.close()

    def save_data(self):
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
            raise DisabledSavingError("Saving to desktop is disabled.")

    def quit(self):
        """Quit and clean up the GoDirect connection."""
        self.godirect.quit()

    def run(self):
        """Run the complete data collection process."""
        if self.connect_to_device():
            self.start_reading()
            self.collect_data()
            self.stop_device()
            self.save_data()
            self.quit()
