from csiapi import csiutils,utils,ops
import pandas as pd
import math

# SapModel = csiutils.attach()

def main(SapModel):
    # defining the property frame which has depth and width
    prop_df = csiutils.get_frameprop(SapModel)
    prop_df.iloc[:,2:] = prop_df.iloc[:,2:].round(5)*1000 #data in mm

    beam_df = []
    column_df = []
    for i in prop_df.Frame_Name:
        beam_list = csiutils.get_beamrebar(SapModel,i)
        beam_list.insert(1, i)
        column_list = csiutils.get_colrebar(SapModel,i)
        column_list.insert(1, i)
        
        beam_df.append(beam_list[1:]) #ignoreing ret
        column_df.append(column_list[1:]) #ignoreing ret

    columnrebar_df = pd.DataFrame(column_df,columns = ["Frame_Name","MatPropLong", "MatPropConfine", "Pattern", "ConfineType", "Cover", \
                        "NumberCBars", "NumberR3Bars", "NumberR2Bars", "RebarSize","TieSize", "TieSpacingLongit", "Number2DirTieBars",\
                            "Number3DirTieBars", "ToBeDesigned"])


    rect_prop_column_df = prop_df[prop_df['PropType'] == ops.etabs.eFramePropType.Rectangular]
    rect_column_rebar_df = columnrebar_df[(columnrebar_df.Pattern == 1) & (columnrebar_df.ToBeDesigned == False)] \
                                                # pattern 1 is for rectangular and to be designed false catches column

    rect_column_df = rect_column_rebar_df.copy() # create a copy to avoid warning
    rect_column_df["width"] = rect_prop_column_df.width # adding width from property
    rect_column_df["depth"] = rect_prop_column_df.depth
    rect_column_df = rect_column_df.iloc[:, [0, 7, 8, 9, 15, 16]]

    circ_prop_column_df = prop_df[prop_df['PropType'] == ops.etabs.eFramePropType.Circle]
    circ_column_rebar_df = columnrebar_df[(columnrebar_df.Pattern == 2) & (columnrebar_df.ToBeDesigned == False)] # pattern 2 is for rectangular

    circ_column_df = circ_column_rebar_df.copy() # create a copy to avoid warning
    circ_column_df["width"] = circ_prop_column_df.width
    circ_column_df = circ_column_df.iloc[:, [0, 6, 9, 15]]


    rect_column_df['tot_rebar'] = 2 * rect_column_df['NumberR3Bars'] + 2 * rect_column_df['NumberR2Bars'] - 4 # eq for total rebars in rectangular section
    rect_column_df['rebar_area'] = math.pi * (rect_column_df['RebarSize'].astype(int) ) ** 2 / 4
    rect_column_df["rebar_perc"] = (rect_column_df['tot_rebar'] * rect_column_df['rebar_area'] / (rect_column_df['width'] * rect_column_df['depth']) * 100).round(1)

    circ_column_df['rebar_area'] = math.pi * (circ_column_df['RebarSize'].astype(int) ) ** 2 / 4
    circ_column_df["rebar_perc"] = (circ_column_df['NumberCBars'] * circ_column_df['rebar_area'] / (math.pi * circ_column_df['width'] ** 2 / 4 ) * 100).round(1)




    rect_column_df["Name_derived"] = "C" + rect_column_df["width"].astype(int).astype(str)  + "x" + \
        rect_column_df["depth"].astype(int).astype(str)  + "-" +  rect_column_df["tot_rebar"].astype(str)+ "T" + \
        rect_column_df["RebarSize"].astype(str) +"-"+ rect_column_df["rebar_perc"].astype(str)+"%" 

    circ_column_df["Name_derived"] = "CD" + circ_column_df["width"].astype(int).astype(str)   + "-" +  circ_column_df["NumberCBars"].astype(str)+ "T" + \
        circ_column_df["RebarSize"].astype(str) +"-"+ circ_column_df["rebar_perc"].astype(str)+"%" 

    # rect_column_df = rect_column_df.drop(["NumberR3Bars","NumberR2Bars","rebar_area"],axis=1)
    rect_column_df = pd.DataFrame(rect_column_df,columns = ["Frame_Name","Name_derived"])
    # circ_column_df = circ_column_df.drop(["rebar_area"],axis=1)
    circ_column_df = pd.DataFrame(circ_column_df,columns = ["Frame_Name","Name_derived"])

    frame_df = pd.concat([rect_column_df,circ_column_df],axis = 0)

    print("Warning!!!The program doesnot diffrentiate corner and edge rebars")
    utils.pretty_print(frame_df)




