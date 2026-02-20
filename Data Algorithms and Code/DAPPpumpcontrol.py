import serial
import time
import logging
import pandas as pd
import DAPPpumpcontrolfunctions as dapp

# -------------------------------
# CONFIGURE SERIAL PORTS (Change as needed)
# -------------------------------
GLUCOSE_PUMP_PORT = "COM3"  # Replace with actual COM port
BUFFER_PUMP_PORT = "COM4"   # Replace with actual COM port
BAUDRATE = 9600  # Harvard Apparatus standard baud rate

# --------------------
#   START RUNNING
# --------------------

# Connect both pumps
glucose_pump = dapp.initialize_serial(GLUCOSE_PUMP_PORT)
buffer_pump = dapp.initialize_serial(BUFFER_PUMP_PORT)

#read .csv file
dapp.read_concentration_csv("test.csv")



# -------------------------------
# RUN A TEST EXPERIMENT
# -------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Enable logging

    # Example: Infuse glucose at 5 mL/min and buffer at 10 mL/min, with 20 mm syringe
    dapp.control_pumps(glucose_rate=5, buffer_rate=10, syringe_diameter=20)

    # Close serial connections
    glucose_pump.close()
    buffer_pump.close()
    logging.info("Serial connections closed.")




# I want my max concentration to be 33 mmol/L
