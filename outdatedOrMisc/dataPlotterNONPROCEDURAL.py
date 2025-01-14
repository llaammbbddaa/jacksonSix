# plotting data from COMPLETE txt files
# Johnny Sarrouf
# 1 / 8 / 2025
# data must be correctly formatted
# volt V, curr mA, temp1 C, temp2 C, hum%

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

# Step 1: Parse the data
file_path = 'testData.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Skip header and parse values
data = [line.strip().split(', ') for line in lines[1:]]
volt = [float(row[0].split()[0]) for row in data]
curr = [float(row[1].split()[0]) for row in data]
temp1 = [float(row[2].split()[0]) for row in data]
temp2 = [float(row[3].split()[0]) for row in data]
hum = [float(row[4].strip('%')) for row in data]

# Generate time in seconds (assuming each row is 1 second apart)
time = list(range(len(data)))

# Step 2: Create a figure for each variable
variables = {"Voltage (V)": volt, "Current (mA)": curr,
             "Temperature 1 (C)": temp1, "Temperature 2 (C)": temp2,
             "Humidity (%)": hum}

figures = []
for var_name, values in variables.items():
    fig, ax = plt.subplots(figsize=(4, 3))  # Set a base size for the plots
    ax.plot(time, values, label=var_name, marker='o')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(var_name)
    ax.set_title(f'{var_name} Over Time')
    ax.legend()
    ax.grid(True)
    figures.append(fig)

# Step 3: Create a resizable Tkinter application
app = ctk.CTk()
app.geometry('1000x800')
app.title('Data Visualization')

# Configure grid layout
rows = len(figures) // 2 + len(figures) % 2  # Two graphs per row
columns = 2
for i in range(rows):
    app.grid_rowconfigure(i, weight=1)
for j in range(columns):
    app.grid_columnconfigure(j, weight=1)

# Add plots to the grid
for idx, fig in enumerate(figures):
    row, col = divmod(idx, columns)
    frame = ctk.CTkFrame(app)
    frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

app.mainloop()

