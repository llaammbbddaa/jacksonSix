# Pico Instrumentality Project

# graphData_PIP
# a massive class for threading and graphing the data
# through custumtkinter and matplotlib
# Johnny Sarrouf and David Jack Jackson
# 1 / 10 / 2025

import customtkinter as ctk
import threading
import pandas as pd
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Define the main class for graphing data
class GraphData:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True)
        # Create a Matplotlib figure and canvas to embed in the Tkinter frame
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Initialize data lists
        self.time_data = []
        self.volt_data = []
        self.curr_data = []
        self.temp1_data = []
        self.temp2_data = []
        self.hum_data = []

    def update_graph(self, filename):
        # Function to update the graph
        start_time = time.time() # Record the start time for time-based x-axis
        while True:
            time.sleep(1)  # Simulate real-time updates
            try:
                # Read new data and update the graph
                new_data = pd.read_csv(filename, header=None, names=['volt V', 'curr mA', 'temp1 C', 'temp2 C', 'hum%'])

                # Check if the DataFrame is not empty
                if new_data.empty:
                    print("CSV file is empty. Waiting for new data...")
                    continue

                # Ensure all required columns are present
                required_columns = ['volt V', 'curr mA', 'temp1 C', 'temp2 C', 'hum%']
                if not all(col in new_data.columns for col in required_columns):
                    print("CSV file is missing required columns. Check file format.")
                    continue

                # Append the latest values to the data lists
                self.time_data.append(time.time() - start_time)
                self.volt_data.append(new_data['volt V'].iloc[-1])
                self.curr_data.append(new_data['curr mA'].iloc[-1])
                self.temp1_data.append(new_data['temp1 C'].iloc[-1])
                self.temp2_data.append(new_data['temp2 C'].iloc[-1])
                self.hum_data.append(new_data['hum%'].iloc[-1])

                # Update the plot
                self.ax.clear()
                self.ax.plot(self.time_data, self.volt_data, label="Voltage (V)")
                self.ax.plot(self.time_data, self.curr_data, label="Current (mA)")
                self.ax.plot(self.time_data, self.temp1_data, label="Temp1 (C)")
                self.ax.plot(self.time_data, self.temp2_data, label="Temp2 (C)")
                self.ax.plot(self.time_data, self.hum_data, label="Humidity (%)")
                self.ax.legend()
                self.canvas.draw()
            except Exception as e:
                print(f"Error updating graph: {e}")

    def threading(self, filename):
        # Start a thread for update_graph
        thread = threading.Thread(target=self.update_graph, args=(filename,))
        thread.daemon = True # Set thread as daemon so it exits when the main program does
        time.sleep(3) # Add a delay before starting the thread
        thread.start()
