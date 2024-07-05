from collections import Counter
import sys

from csiapi import csiutils,ops

SapModel = csiutils.attach()
df_select = csiutils.get_selection(SapModel)
csiutils.clear_selection(SapModel)  #clear previous selection if any

if df_select.object_typename.any():
    obj_type = input("Enter one of the following: Frame, Area : ")
    list_items = df_select[df_select.object_typename == obj_type].unique_label
    floor_obj, wall_obj, col_obj, beam_obj, brace_obj  = ([] for i in range(5)) #assigning empty list

    if obj_type == "Area":
        area_type = input('Enter one of the following: Floor, Wall :')
        for i in list_items: #seperating elements into the basic form
            if csiutils.area_type(SapModel,i) in ["Floor", "Null"]:
                floor_obj.append(i)
            elif csiutils.area_type(SapModel,i) == "Wall":
                wall_obj.append(i)
            
        if area_type == "Wall":
            for i in wall_obj:
                ops.set_areaselection(SapModel,i)
        elif area_type == "Floor":
            for i in floor_obj:
                ops.set_areaselection(SapModel,i)
    
    elif obj_type == "Frame":
        frame_type = input('Enter one of the following: Column, Beam, Brace :')
        for i in list_items: #seperating elements into the basic form
            if csiutils.member_type(SapModel,i) == "Column":
                col_obj.append(i)
            elif csiutils.member_type(SapModel,i) == "Beam":
                beam_obj.append(i)
            elif csiutils.member_type(SapModel,i) == "Brace":
                brace_obj.append(i)

        if frame_type == "Column":
            for i in col_obj:
                ops.set_frameselection(SapModel,i)
        elif frame_type == "Beam":
            for i in beam_obj:
                ops.set_frameselection(SapModel,i)
        elif frame_type == "Brace":
            for i in brace_obj:
                ops.set_frameselection(SapModel,i)
else:
    print("No Elements selected")
    sys.exit()

csiutils.refresh(SapModel)
print("Succesfully selected")