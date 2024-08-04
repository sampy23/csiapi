from csiapi import csiutils

# SapModel = csiutils.attach()

def main (SapModel):
    counter = 0
    for i in csiutils.frame_all(SapModel):
        if csiutils.member_type(SapModel,i) == "Brace":
            ret, point1, point2 = SapModel.FrameObj.GetPoints(i,str(),str())

            ret, X1, Y1, Z1 = SapModel.PointObj.GetCoordCartesian (point1,float(),float(),float())
            ret, X2, Y2, Z2 = SapModel.PointObj.GetCoordCartesian (point2,float(),float(),float())
            if Z1 != Z2:
                print(f"Vertical bracing found, possible inclined column {i}")
            else:
                counter+=1
            
    if not counter:
        print("No vertical bracing/inclined column found in the model")