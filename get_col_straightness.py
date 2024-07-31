from csiapi import csiutils,ops,utils

SapModel = csiutils.attach()

for i in csiutils.frame_all(SapModel):
    if csiutils.member_type(SapModel,i) == "Brace":
        ret, point1, point2 = SapModel.FrameObj.GetPoints(i,str(),str())

        ret, X1, Y1, Z1 = SapModel.PointObj.GetCoordCartesian (point1,float(),float(),float())
        ret, X2, Y2, Z2 = SapModel.PointObj.GetCoordCartesian (point2,float(),float(),float())
        if Z1 != Z2:
            print(f"Vertical bracing found, possible inclined column {i}")