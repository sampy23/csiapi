from csiapi import csiutils

# SapModel = csiutils.attach()

def main (SapModel):
    counter = 0
    for i in csiutils.frame_all(SapModel):
        if (csiutils.member_type(SapModel,i) == "Column") or (csiutils.member_type(SapModel,i) == "Brace"):
            ret, point1, point2 = SapModel.FrameObj.GetPoints(i,str(),str())

            ret, X1, Y1, Z1 = SapModel.PointObj.GetCoordCartesian (point1,float(),float(),float())
            ret, X2, Y2, Z2 = SapModel.PointObj.GetCoordCartesian (point2,float(),float(),float())
            if csiutils.member_type(SapModel,i) == "Brace":
                if Z1 != Z2: # to filter out plan bracings
                    print(f"Vertical bracing found, possible inclined column {i}")
                else:
                    counter+=1
            elif csiutils.member_type(SapModel,i) == "Column":
                if (X1 != X2) or (Y1 != Y2) :
                    print(f"Inclined column found for member {i}")
                else:
                    counter+=1 
    if not counter:
        print("No vertical bracing/inclined column found in the model")