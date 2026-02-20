import serial
import time
import logging
import pandas as pd

# -------------------------------
# CONFIGURE SERIAL PORTS (Change as needed)
# -------------------------------
GLUCOSE_PUMP_PORT = "COM3"  # Replace with actual COM port
BUFFER_PUMP_PORT = "COM4"   # Replace with actual COM port
BAUDRATE = 9600  # Harvard Apparatus standard baud rate

# -------------------------------
# INITIALIZE SERIAL CONNECTION
# -------------------------------
def initialize_serial(port):
    """Initialize RS-232 serial communication with the pump."""
    logging.info(f"Trying to connect for pump {port}")
    try:
        ser = serial.Serial(port, baudrate=BAUDRATE, stopbits=2, timeout=2)
        logging.info(f"Connected to pump on {port}")
        return ser
    except Exception as e:
        logging.error(f"Error connecting to pump on {port}: {e}")
        exit()

# -------------------------------
# SEND COMMANDS TO PUMPS
# -------------------------------
def send_command(pump, command):
    """Send a command to the pump and return the response."""
    pump.write((command + "\r").encode())  # Append carriage return
    time.sleep(0.1)  # Allow time for processing
    response = pump.read_all().decode().strip()
    logging.info(f"Sent: {command} | Response: {response}")
    return response

def set_flow_rate(pump, rate, units="MM"):
    """Set the pump's flow rate (Default: mL/min)."""
    send_command(pump, f"RAT {rate} {units}")

def set_syringe_diameter(pump, diameter = 1.5):
    """Set the syringe diameter (mm)."""
    send_command(pump, f"DIA {diameter}")

def start_pump(pump):
    """Start the pump infusion."""
    send_command(pump, "RUN")

def stop_pump(pump):
    """Stop the pump."""
    send_command(pump, "STP")

def get_status(pump):
    """Get pump status."""
    return send_command(pump, "DIS")

# -------------------------------
# GET DATA FROM USER
# -------------------------------
import pandas as pd

def read_concentration_csv(filepath):
    """
    Reads a CSV file and extracts concentration data.
    
    Parameters:
    - filepath (str): Path to the CSV file.

    Returns:
    - concentrations (list): List of concentration values from the CSV.
    - time_values (list): List of time values if available, else None.
    """
    try:
        # Read CSV file
        df = pd.read_csv(filepath)

        # Automatically detect the column containing concentrations
        concentration_columns = [col for col in df.columns if "concentration" in col.lower()]
        
        if not concentration_columns:
            raise ValueError("No concentration column found in the CSV file.")

        # Extract concentration data (assume first matching column)
        concentrations = df[concentration_columns[0]].tolist()
        
        # Try to extract time values if a "time" column exists
        time_columns = [col for col in df.columns if "time" in col.lower()]
        time_values = df[time_columns[0]].tolist() if time_columns else None
        
        print(f"Successfully read {len(concentrations)} data points from {filepath}")
        print (concentrations[0])
        return time_values, concentrations

    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def calculate_delay(PBS_FLOWRATE, GLUCOSE_FLOWRATE, LENGTH):
    PBS_TIME = LENGTH/PBS_FLOWRATE
    GLUCOSE_TIME = LENGTH/GLUCOSE_FLOWRATE
    GLUCOSE_DELAY = max(0, (PBS_TIME-GLUCOSE_TIME))
    PBS_DELAY = max(0, (GLUCOSE_TIME-PBS_TIME))
    return GLUCOSE_DELAY, PBS_DELAY
        


# -------------------------------
# SET UP AND RUN PUMPS
# -------------------------------
def control_pumps(glucose_rate, buffer_rate, syringe_diameter):
    """Control both pumps dynamically."""
    
    # Set syringe diameter (Ensure both pumps use the same syringe size)
    set_syringe_diameter(glucose_pump, syringe_diameter)
    set_syringe_diameter(buffer_pump, syringe_diameter)

    # Set initial flow rates
    set_flow_rate(glucose_pump, glucose_rate)
    set_flow_rate(buffer_pump, buffer_rate)

    # Start both pumps
    start_pump(glucose_pump)
    start_pump(buffer_pump)
    
    logging.info(f"Pumps started | Glucose: {glucose_rate} mL/min | Buffer: {buffer_rate} mL/min")

    # Run for a fixed time, then stop
    time.sleep(60)  # Adjust based on experiment duration
    
    stop_pump(glucose_pump)
    stop_pump(buffer_pump)

    logging.info("Pumps stopped")


