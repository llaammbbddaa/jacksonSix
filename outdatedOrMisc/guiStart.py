# Data Visualization for PICO
# Johnny Sarrouf
# 1 / 8 / 2025
# to visualize data gathered on pico, with gui

import customtkinter

def start():
    print("process started")
    
def stop():
    print("process ended")

app = customtkinter.CTk()
app.title("data visualization")
app.geometry("550x400")

button1 = customtkinter.CTkButton(app, text="start", command=start)
button1.grid(row=0, column=0, padx=20, pady=20)
button2 = customtkinter.CTkButton(app, text="stop", command=stop)
button2.grid(row=0, column=1, padx=20, pady=20)

app.mainloop()
