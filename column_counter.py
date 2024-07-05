from collections import Counter
import pandas as pd

from csiapi import csiutils, utils

SapModel = csiutils.attach()
df_select = csiutils.get_selection(SapModel)
list_frames = df_select[df_select.object_typename == "Frame"].unique_label

if list_frames.any():
    column_list = []
    for i in list_frames:
        if csiutils.member_type(SapModel,i) == "Column":
            sec_name = csiutils.get_section(SapModel,i)
            column_list.append(sec_name)
    
    summary = utils.organise(column_list)
    print(summary)
else:
    print("No members selected")