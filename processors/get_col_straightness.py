from csiapi import csiutils,ops

# SapModel = csiutils.attach()

def main (SapModel):
    found = False
    frame_list = []
    for i in csiutils.frame_all(SapModel):
        if (csiutils.member_type(SapModel,i) == "Column") or (csiutils.member_type(SapModel,i) == "Brace"):
            ret, point1, point2 = SapModel.FrameObj.GetPoints(i,str(),str())

            ret, X1, Y1, Z1 = SapModel.PointObj.GetCoordCartesian (point1,float(),float(),float())
            ret, X2, Y2, Z2 = SapModel.PointObj.GetCoordCartesian (point2,float(),float(),float())
            if csiutils.member_type(SapModel,i) == "Brace":
                if Z1 != Z2: # to filter out plan bracings
                    print(f"Vertical bracing found, possible inclined column {i}")
                    frame_list.append(i)
                    found = True
            elif csiutils.member_type(SapModel,i) == "Column":
                if (X1 != X2) or (Y1 != Y2) :
                    print(f"Inclined column found for member {i}")
                    frame_list.append(i)
                    found = True

    if found:
        print("Vertical bracing/inclined column found in the model!!!")
        csiutils.clear_selection(SapModel)
        [ops.set_frameselection(SapModel,i) for i in frame_list]
    else:
        print("No vertical bracing/inclined column found in the model")