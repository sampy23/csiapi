NAME = "Select Column by Axial force"
DESCRIPTION = "Programs runs and designs the model and then allow user to select columns in particular range."
REQUIRES_MODEL = True

import pandas as pd
import matplotlib.pyplot as plt

from csiapi import csiutils,ops,utils
import ETABSv1 as etabs

def local():
    input("Selection will be based on the combinations selected in the table of etabs model, press enter to continue: ")
    # for some reason following will not work
    # deselect all combo
    # ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    # combo_list = utils.read_txt\
    #         (r'C:\Users\Shahabaz.muhammed\OneDrive - Surbana Jurong Private Limited\.python\etabs\support_files\combos.txt')
    # [SapModel.Results.Setup.SetComboSelectedForOutput(i,True) for i in combo_list]
    # for i in combo_list:
    #     check_combo = ops.set_combo(SapModel,i)
    #     if check_combo:
    #         pass
    #     else:
    #         print(f"Combination {i} not selected")
    
    SapModel = csiutils.attach()
    csiutils.run(SapModel)
    csiutils.set_units(SapModel) # set to kNmc

    design_concrete = ops.DesignConcrete(SapModel)

    df = design_concrete.all_column_design_forces()
    df["P"] = pd.to_numeric(df["P"], errors="coerce") # to force dataframe which are not numeric to number

    # ----------------------------------
    # FIND CONTROLLING LOAD COMBINATION FOR COMPRESSION
    # ----------------------------------

    compression = df.groupby("Unique_Name")["P"].min() # targetting only compression

    frame_max = compression.idxmax()
    frame_min = compression.idxmin()

    p_maxima = float(compression.max())
    p_minima = float(compression.min())

    print("\nGoverning compression forces (10 most critical):\n")

    print(
        compression.sort_values().head(10)
    )

    print(f"\nMaximum axial load: {frame_max} → {p_maxima:.2f} kN")
    print(f"Minimum axial load: {frame_min} → {p_minima:.2f} kN")

    # ----------------------------------
    # HISTOGRAM (LOAD DISTRIBUTION)
    # ----------------------------------

    plt.hist(compression.dropna(), bins=15)
    plt.title("Column Axial Load Distribution")
    plt.xlabel("Axial Force (kN)")
    plt.ylabel("Number of Columns")
    plt.show()


    while True:
        print(f"\nMinima is {p_minima:.2f}kN, Maxima is {p_maxima:.2f}kN")
        lower_bound = utils.input_float("\nEnter the lower bound of the P value for member selection: ",\
                            p_minima,p_maxima, \
                            reminder="Please enter number which are within the maxima and minima obtained.")
        upper_bound = utils.input_float("Enter the upper bound of the P value for member selection: ",\
                            p_minima,p_maxima, \
                            reminder="Please enter number which are within the maxima and minima obtained.")

        if lower_bound > upper_bound: # Handling user mistake in upper and lower bound
            lower_bound, upper_bound = upper_bound, lower_bound
        
        # --- SELECT MEMBERS ---
        selected_max = compression[(compression >= lower_bound) & (compression <= upper_bound)]
        # selected_min = pmin[(pmin >= lower_bound) & (pmin <= upper_bound)]
        selected_cols = list(set(
            selected_max.index.tolist()
        ))

        print(f"\nSelecting {len(selected_cols)} columns...")
        SapModel.SelectObj.ClearSelection()
        ops.set_frameselection(SapModel, selected_cols)

        check_exit = input("\nPress Enter to continue and q to exit: ")
        if check_exit.lower() == "q":
            break
        else:
            continue


if __name__ == "__main__":
    local()
