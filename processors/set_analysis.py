import tkinter as tk
from tkinter import messagebox

from csiapi import csiutils

def Mbox(title, message):
    # Create a root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ensure the dialog stays on top
    root.attributes("-topmost", True)
    
    # Show a messagebox with a warning message
    messagebox.showwarning(title, message)
    
    # Destroy the root window after the messagebox is closed
    root.destroy()

def main(SapModel):
    ret = csiutils.run(SapModel)

    if not ret:
        Mbox("ETABS Run Status", "Analysis Complete!!")
    else:
        Mbox("ETABS Run Status", "Analysis Incomplete!!")

if __name__ == "__main__":
    SapModel = csiutils.attach()
    main(SapModel)