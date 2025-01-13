# PURELY FOR TESTING PURPOSES
# mainCOMP.py file version 2
# main file for computer side
# Johnny Sarrouf and David Jack Jackson
# 1 / 9 / 25

import pS_COMP_PIP
import serialSave_PIP
from graphData_PIP import GraphData
import customtkinter as ctk
import time

def main():
    # Initialize serial communication with the Pico
    pico = pS_COMP_PIP.beginSerial()
    # Open a file for saving serial data
    file = serialSave_PIP.beginFile()
    fileName = serialSave_PIP.getFileName(file)

    # Initialize the GUI application
    app = ctk.CTk()
    graph = GraphData(app)

    # Correct call to threading
    graph.threading(fileName)

    try:
        # Main loop for reading and writing data
        while True:
            serialSave_PIP.beginWrite(pico, file) # Write serial data to the file
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle the program's exit when interrupted (Ctrl+C)
        file.close()
        pS_COMP_PIP.pleaseStop(pico) # Stop Pico communication safely
        print("Program safely exited")

    # Start the GUI main loop to display the application
    app.mainloop()

# Entry point of the program
if __name__ == "__main__":
    main()
