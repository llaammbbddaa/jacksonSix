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
    pico = pS_COMP_PIP.beginSerial()
    file = serialSave_PIP.beginFile()
    fileName = serialSave_PIP.getFileName(file)

    app = ctk.CTk()
    graph = GraphData(app)

    # Correct call to threading
    graph.threading(fileName)

    try:
        while True:
            serialSave_PIP.beginWrite(pico, file)
            time.sleep(1)
    except KeyboardInterrupt:
        file.close()
        pS_COMP_PIP.pleaseStop(pico)
        print("Program safely exited")

    app.mainloop()

if __name__ == "__main__":
    main()
