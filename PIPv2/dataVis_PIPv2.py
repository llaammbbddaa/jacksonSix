import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Function to initialize the GUI
def create_gui(pico, data, data_lock):
    # Create the main application window
    app = ctk.CTk()
    app.title("Real-Time Data Visualization")
    app.geometry("800x600")

    # Create the main frame for the plot
    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Create a Matplotlib figure and subplots
    fig, axes = plt.subplots(3, 1, figsize=(8, 6))
    fig.tight_layout(pad=3.0)

    # Embed the Matplotlib figure in the CustomTkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    # Start the threads
    threading.Thread(target=read_serial_data, args=(pico, data, data_lock), daemon=True).start()
    threading.Thread(target=update_plot, args=(axes, canvas, data, data_lock), daemon=True).start()

    # Start the CustomTkinter event loop
    app.mainloop()

# Function to read serial data
def read_serial_data(pico, data, data_lock):
    while True:
        try:
            line = pico.readline().decode("utf-8").strip()
            values = [float(x) for x in line.split(",")]

            with data_lock:
                data["time"].append(time.time())  # Use a timestamp
                data["voltage"].append(values[0])
                data["current"].append(values[1])
                data["temperature1"].append(values[2])
                data["temperature2"].append(values[3])
                data["humidity"].append(values[4])

                # Keep the data buffer within a reasonable size (e.g., last 100 points)
                for key in data.keys():
                    if len(data[key]) > 100:
                        data[key].pop(0)
        except Exception as e:
            print(f"Error reading serial data: {e}")

# Function to update the plot
def update_plot(axes, canvas, data, data_lock):
    while True:
        with data_lock:
            # Clear and redraw the plots
            axes[0].clear()
            axes[0].plot(data["time"], data["voltage"], label="Voltage (V)")
            axes[0].set_title("Voltage")
            axes[0].set_xlabel("Time (s)")
            axes[0].set_ylabel("Voltage (V)")
            axes[0].legend()

            axes[1].clear()
            axes[1].plot(data["time"], data["current"], label="Current (mA)")
            axes[1].set_title("Current")
            axes[1].set_xlabel("Time (s)")
            axes[1].set_ylabel("Current (mA)")
            axes[1].legend()

            axes[2].clear()
            axes[2].plot(data["time"], data["humidity"], label="Humidity (%)")
            axes[2].set_title("Humidity")
            axes[2].set_xlabel("Time (s)")
            axes[2].set_ylabel("Humidity (%)")
            axes[2].legend()

        canvas.draw()
        time.sleep(1)  # Update the plot every second
