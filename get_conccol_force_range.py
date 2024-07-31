import pandas as pd

from csiapi import csiutils,ops,utils
import ETABSv1 as etabs

SapModel = csiutils.attach()
csiutils.run(SapModel)
csiutils.set_units(SapModel) # set to kNmc

design_concrete = ops.DesignConcrete(SapModel)
frame_obj = etabs.cFrameObj(SapModel.FrameObj)

input("Selection will be based on the combinations selected in the table of etabs model, press enter to continue")
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

p_design_list = []
frame_list = csiutils.frame_all(SapModel)
for i in frame_list:
    mem_type = csiutils.member_type(SapModel,i)
    if mem_type == "Column":
        conccolumn_design_df = design_concrete.col_concdesign_forces(i)
        p_design_list.append(round(conccolumn_design_df.P.abs().max(),1))

inx_max = p_design_list.index(max(p_design_list))
inx_min = p_design_list.index(min(p_design_list))

p_minima = min(p_design_list)
p_maxima = max(p_design_list)
print(f"\nMaximum axial load is for {frame_list[inx_max]}, with force of {p_maxima}kN")
print(f"Lowest axial load is for {frame_list[inx_min]}, with force of {p_minima}kN")

print(f"\nMinima is {p_minima}kN, Maxima is {p_maxima}kN")
lower_bound = utils.input_float("\nEnter the lower bound of the P value for member selection: ",\
                    p_minima,p_maxima, \
                    reminder="Please enter number which are within the maxima and minima obtained.")
upper_bound = utils.input_float("Enter the upper bound of the P value for member selection: ",\
                    p_minima,p_maxima, \
                    reminder="Please enter number which are within the maxima and minima obtained.")

select_list = []
csiutils.clear_selection(SapModel)
for i,j in zip(frame_list,p_design_list):
    if (j <= upper_bound) and (j >= lower_bound):
        select_list.append(i)
        ops.set_frameselection(SapModel,i)

if select_list:
    print("\nSuccesfully selected members in model")
else:
    print("\nNo members selected as no members could be found in this range")
