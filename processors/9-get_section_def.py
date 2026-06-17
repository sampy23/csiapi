NAME = "Frame Count"
DESCRIPTION = "Creates a list detailing the frame name and how many are currently selected"
REQUIRES_MODEL = True

from collections import Counter
import pandas as pd

from csiapi import csiutils,utils

def main(SapModel):
    df_select = csiutils.get_selection(SapModel)
    list_frames = df_select[df_select.object_typename == "Frame"].unique_label

    if list_frames.any():
        selec_obj = []
        for i in list_frames:
            sec_name = csiutils.get_section(SapModel,i)
            selec_obj.append(sec_name)
        
        summary = utils.organise(selec_obj)
        summary.rename_axis('Frame_name', inplace=True)
        return summary
    return None

if __name__ == "__main__":
    SapModel = csiutils.attach()
    main(SapModel)