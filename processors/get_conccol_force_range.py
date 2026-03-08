NAME = "Select Column by Axial force"
DESCRIPTION = "Programs runs and designs the model and then allow user to select columns in particular range."
REQUIRES_MODEL = True

import pandas as pd

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

  # Maximum absolute axial load per column
    pmax = df.groupby("Unique_Name")["P"].max()
    pmin = df.groupby("Unique_Name")["P"].min() #critical as this is compression

    # Global maxima/minima
    frame_max = pmax.idxmax()
    frame_min = pmin.idxmin()

    p_maxima = pmax.max()
    p_minima = pmin.min()

    print(f"\nMaximum axial load is for {frame_max}, with force of {p_maxima:.2f}kN")
    print(f"Lowest axial load is for {frame_min}, with force of {p_minima:.2f}kN")

    while True:
        print(f"\nMinima is {p_minima}kN, Maxima is {p_maxima}kN")
        lower_bound = utils.input_float("\nEnter the lower bound of the P value for member selection: ",\
                            p_minima,p_maxima, \
                            reminder="Please enter number which are within the maxima and minima obtained.")
        upper_bound = utils.input_float("Enter the upper bound of the P value for member selection: ",\
                            p_minima,p_maxima, \
                            reminder="Please enter number which are within the maxima and minima obtained.")

        if lower_bound > upper_bound: # Handling user mistake in upper and lower bound
            lower_bound, upper_bound = upper_bound, lower_bound
        
        # --- SELECT MEMBERS ---
        selected_max = pmax[(pmax >= lower_bound) & (pmax <= upper_bound)]
        selected_min = pmin[(pmin >= lower_bound) & (pmin <= upper_bound)]
        selected_cols = selected_max.index.tolist()
        selected_cols = list(set(
            selected_max.index.tolist() + selected_min.index.tolist()
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
