import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import serial
import threading
import datetime
import os

# Step 1: Setup Serial Communication
SERIAL_PORT = 'COM9'  # Adjust this to your port
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)

# Create a timestamped log file
now = datetime.datetime.now()
formatted_date_time = now.strftime("%m_%d_%Y %I_%M_%S %p") + ".txt"
if os.path.exists(formatted_date_time):
    file = open(formatted_date_time, "a")
    file.write("\n")
else:
    file = open(formatted_date_time, "w")
    #file.write("volt V, curr mA, temp1 C, temp2 C, hum%\n")
    file.write("laser volt V, laser curr mA, laser temp C, opc volt V, opc curr mA, opc temp C, hum%\n")

# Shared data structure for live updates
# laser and optical power converter
data = {
    "time": [],
    "Voltage (V) Laser": [],
    "Current (mA) Laser": [],
    "Temperature (C) Laser": [],
    "Voltage (V) OPC": [],
    "Current (mA) OPC": [],
    "Temperature (C) OPC": [],
    "Humidity (%)": None  # Store the latest humidity value
}

# Lock for safe data access
data_lock = threading.Lock()

# Function to read serial data
def read_serial_data():
    elapsed_time = 0
    while True:
        try:
            line = ser.readline().decode("utf-8").strip()
            if line:
                file.write(line + "\n")
                values = line.split(', ')
                with data_lock:
                    data["time"].append(elapsed_time)
                    data["Voltage (V) Laser"].append(float(values[0].split()[0]))
                    data["Current (mA) Laser"].append(float(values[1].split()[0]))
                    data["Temperature (C) Laser"].append(float(values[2].split()[0]))
                    data["Voltage (V) OPC"].append(float(values[0].split()[0]))
                    data["Current (mA) OPC"].append(float(values[1].split()[0]))
                    data["Temperature (C) OPC"].append(float(values[3].split()[0]))
                    data["Humidity (%)"] = float(values[4].strip('%'))  # Store the latest humidity
                    elapsed_time += 1
        except (ValueError, IndexError):
            print(f"Error parsing line: {line}")
        except serial.SerialException:
            print("Serial connection error. Exiting...")
            break

# Function to dynamically update graphs and humidity display
def update_graphs():
    while True:
        with data_lock:
            if data["time"]:
                for ax, var_name in zip(axes, list(data.keys())[1:-1]):  # Skip "time" and "Humidity (%)"
                    ax.clear()
                    ax.plot(data["time"], data[var_name], label=var_name)
                    ax.set_title(var_name)
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel(var_name)
                    ax.grid(True)
                    ax.legend()
                # Update the humidity label
                if data["Humidity (%)"] is not None:
                    humidity_label.configure(text=f"Humidity: {data['Humidity (%)']:.2f}%")
        canvas.draw()

# Step 2: Setup GUI with CustomTkinter
app = ctk.CTk()
app.geometry("1000x800")
app.title("Live Data Visualization")

frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True)

# Humidity label at the top-left corner
humidity_label = ctk.CTkLabel(app, text="Humidity: N/A", font=("Arial", 16))
humidity_label.place(x=20, y=20)

# Step 3: Create matplotlib figure and axes
fig, axes = plt.subplots(2, 3, figsize=(10, 8))  # Create a 2x3 grid for six graphs
axes = axes.flatten()

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# Step 4: Start threads for serial reading and graph updating
serial_thread = threading.Thread(target=read_serial_data, daemon=True)
update_thread = threading.Thread(target=update_graphs, daemon=True)

serial_thread.start()
update_thread.start()

# Run the app
app.mainloop()

# Close the file after the app exits
file.close()

