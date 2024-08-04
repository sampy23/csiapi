from csiapi import csiutils, utils

def main (SapModel):
    df_select = csiutils.get_selection(SapModel)
    list_frames = df_select[df_select.object_typename == "Frame"].unique_label

    if list_frames.any():
        column_list = []
        for i in list_frames:
            if csiutils.member_type(SapModel,i) == "Column":
                sec_name = csiutils.get_section(SapModel,i)
                column_list.append(sec_name)
        
        summary = utils.organise(column_list)
        # Assign a name to the index
        summary.rename_axis('Frame_name', inplace=True)
        utils.pretty_print(summary)
        csiutils.clear_selection(SapModel)
    else:
        print("No members selected")

if __name__ == "__main__":
    SapModel = csiutils.attach()
    main(SapModel)