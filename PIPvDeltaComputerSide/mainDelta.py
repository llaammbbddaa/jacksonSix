# mainPLEASEWORK.py
# computer side
# main file, will host the graphing on the main thread, and then everything else onto a different thread (threading)
# Johnny Sarrouf and David Jack Jackson
# 1 / 13 / 2025

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import serial
import threading
import datetime
import os
import queue
#import serialSaveDelta as serialSave not needed because this already saves the data
import pS_COMP_PIP as commandPico


def stopProgram():
    global file, pico
    if file:
        file.close()
    if pico:
        pico.close()
    commandPico.pleaseStop(pico)

def beginSerial(port, baud):
    try:
        pico = serial.Serial(port, baud, timeout=5)
        return pico
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def beginFile():
    # Create a timestamped log file
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%m_%d_%Y %I_%M_%S %p") + ".txt"
    file = open(formatted_date_time, "w")
    file.write("laser volt V, laser curr mA, laser temp C, opc volt V, opc curr mA, opc temp C, hum%\n")
    return file

def beginData():
    # Shared data structure for live updates
    data = {
        "time": [],
        "Voltage (V) Laser": [],
        "Current (mA) Laser": [],
        "Temperature (C) Laser": [],
        "Voltage (V) OPC": [],
        "Current (mA) OPC": [],
        "Temperature (C) OPC": [],
        "Humidity (%)": None
    }

    data_lock = threading.Lock()
    return data, data_lock

# Function to read serial data
def read_serial_data(pico, file, data, data_lock, update_queue):
    elapsed_time = 0
    while True:
        try:
            line = pico.readline().decode("utf-8").strip()
            if line:
                if ("set" not in line and "laser" not in line):
                    file.write(line + "\n")
                    file.flush()
                    values = line.split(', ')
                with data_lock:
                    data["time"].append(elapsed_time)
                    data["Voltage (V) Laser"].append(float(values[0]))
                    data["Current (mA) Laser"].append(float(values[1]))
                    data["Temperature (C) Laser"].append(float(values[2]))
                    data["Voltage (V) OPC"].append(float(values[0]))
                    data["Current (mA) OPC"].append(float(values[1]))
                    data["Temperature (C) OPC"].append(float(values[2]))
                    data["Humidity (%)"] = float(values[3].strip('%'))
                    elapsed_time += 1
                update_queue.put("update")
        except (ValueError, IndexError):
            print(f"Error parsing line: {line}")
        except serial.SerialException:
            print("Serial connection error. Exiting...")
            break

# Function to dynamically update graphs and humidity display
def update_graphs(data, data_lock, update_queue, axes, canvas, humidity_label):
    while True:
        update_queue.get()  # Wait for update signal
        with data_lock:
            if data["time"]:
                for ax, var_name in zip(axes, list(data.keys())[1:-1]):
                    ax.clear()
                    ax.plot(data["time"], data[var_name], label=var_name)
                    ax.set_title(var_name)
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel(var_name)
                    ax.grid(True)
                    ax.legend()
                if data["Humidity (%)"] is not None:
                    humidity_label.configure(text=f"Humidity: {data['Humidity (%)']:.2f}%")
        canvas.draw()

def setupGUI():
    import matplotlib as mpl
    mpl.style.use('dark_background')  # Apply dark mode to the plots
    
    app = ctk.CTk()
    app.geometry("1000x800")
    app.title("Live Data Visualization")

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    humidity_label = ctk.CTkLabel(app, text="Humidity: N/A", font=("Arial", 16))
    humidity_label.place(x=20, y=20)

    fig, axes = plt.subplots(2, 3, figsize=(10, 8))
    axes = axes.flatten()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    return axes, canvas, app, humidity_label


def beginThreading(pico, file, data, data_lock, update_queue, axes, canvas, humidity_label):
    serial_thread = threading.Thread(target=read_serial_data, args=(pico, file, data, data_lock, update_queue), daemon=True)
    update_thread = threading.Thread(target=update_graphs, args=(data, data_lock, update_queue, axes, canvas, humidity_label), daemon=True)

    serial_thread.start()
    update_thread.start()

if __name__ == "__main__":
    pico = beginSerial("COM9", 9600)
    file = beginFile()
    data, data_lock = beginData()
    update_queue = queue.Queue()
    axes, canvas, app, humidity_label = setupGUI()
        
    # begin sending commands to initialize laser stuff
    # will run as a loop until "stop" is sent
    commandPico.beginSend(pico)

    beginThreading(pico, file, data, data_lock, update_queue, axes, canvas, humidity_label)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        stopProgram()
    except:
        stopProgram()
        print("error -> {e}")
