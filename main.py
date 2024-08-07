import sys
import os
import importlib
from csiapi import csiutils

SapModel = csiutils.attach()

processors_dir = 'processors' #to be called from folder which has this folder

# Dynamically import all .py files from the processors directory
modules = {}
for file in os.listdir(processors_dir):
    if file.endswith(".py"):
        module_name = file[:-3]  # Remove .py extension
        module = importlib.import_module(f"{processors_dir}.{module_name}")
        modules[module_name] = module

# Create dictionary mapping selection numbers to modules and their main functions
scripts = {i + 1: module for i, (name, module) in enumerate(modules.items())}

while True:
    try:
        # Dynamically generate the user input prompt string
        input_string = "Enter the following number for the desired action:\n    0  -  Exit\n"
        for i, name in enumerate(modules.keys(), start=1):
            input_string += f"    {i}  -  {name}\n"
        
        selection = int(input(input_string))
        if selection == 0:
            sys.exit()

        elif selection in scripts:
            script = scripts[selection]
            if hasattr(script, 'main'):
                script.main(SapModel)
                input("Press enter to continue: ")
                print("==========================================")
            elif hasattr(script, 'local'):
                script.local()
                input("Press enter to continue: ")
                print("==========================================")
            else:
                print(f"The selected script does not have a 'main' function.")
    except ValueError:
        print("Invalid input. Please enter a number")
    except Exception as e:
        print(f"An error occurred: {e}")