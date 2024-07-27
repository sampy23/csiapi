import pandas as pd

from csiapi import csiutils,ops
import ETABSv1 as etabs

SapModel = csiutils.attach()
csiutils.run(SapModel)
csiutils.set_units(SapModel) # set to kNmc

design_concrete = ops.DesignConcrete(SapModel)
frame_obj = etabs.cFrameObj(SapModel.FrameObj)

P_design_list = []
frame_list = csiutils.frame_all(SapModel)
for i in frame_list:
    mem_type = csiutils.member_type(SapModel,i)
    if mem_type == "Column":
        conccolumn_design_df = design_concrete.col_concdesign_forces(i)
        P_design_list.append(round(conccolumn_design_df.P.abs().max(),1))

inx_max = P_design_list.index(max(P_design_list))
inx_min = P_design_list.index(min(P_design_list))

print(f"Maximum axial load is for {frame_list[inx_max]}, with force of {max(P_design_list)}")
print(f"Lowest axial load is for {frame_list[inx_min]}, with force of {min(P_design_list)}")

lower_bound = float(input ("Enter the lower bound of the P value for member selection: "))
upper_bound = float(input ("Enter the upper bound of the P value for member selection: "))

select_list = []
for i,j in zip(frame_list,P_design_list):
    if (j < upper_bound) and (j > lower_bound):
        select_list.append(i)
        ops.set_frameselection(i)

if select_list:
    print("Succesfully selected")
else:
    print("No members selected")
