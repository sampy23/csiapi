import ctypes
from tkinter import messagebox

from csiapi import csiutils

def Mbox(title, message):
    WS_EX_TOPMOST = 0x40000

    # display a message box; execution will stop here until user acknowledges
    ctypes.windll.user32.MessageBoxExW(None, message, title, WS_EX_TOPMOST)

    print("User clicked OK.")

SapModel = csiutils.attach()
ret = csiutils.run(SapModel)

if not ret:
    Mbox("ETABS Run Message Box", "Analysis Complete!!")
else:
    Mbox("ETABS Run Message Box", "Analysis Incomplete!!")