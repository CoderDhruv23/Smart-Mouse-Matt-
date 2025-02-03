# utils/serial_handler.py
import serial
from threading import Thread, Lock
import time

class SerialManager:
    def __init__(self, port='COM8', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.temperature = None
        self.humidity = None
        self.active_session = False
        self.running = True
        self.lock = Lock()  # Thread-safe data access
        self.ser = None
        
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Connected to {port} successfully!")
            self.thread = Thread(target=self._read_serial)
            self.thread.daemon = True
            self.thread.start()
        except Exception as e:
            print(f"Serial connection failed: {str(e)}")

    def _read_serial(self):
        while self.running:
            try:
                if self.ser and self.ser.in_waiting > 0:
                    line = self.ser.readline().decode().strip()
                    with self.lock:
                        if line.startswith("TEMP:"):
                            parts = line.split(',')
                            self.temperature = float(parts[0].split(':')[1])
                            self.humidity = float(parts[1].split(':')[1])
                        elif line == "TOUCH:WAKE":
                            self.active_session = True
            except Exception as e:
                print(f"Serial read error: {str(e)}")
                time.sleep(1)

    def get_sensor_data(self):
        """Get fresh sensor data thread-safely"""
        with self.lock:
            return self.temperature, self.humidity

    def __del__(self):
        self.running = False
        if self.ser:
            self.ser.close()