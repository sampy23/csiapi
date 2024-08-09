from collections import Counter
import pandas as pd
from collections.abc import Iterable

from csiapi import csiutils,ops, utils

# SapModel = csiutils.attach()

def material_data(SapModel):
    mat_name = list(csiutils.get_names(SapModel))
    mat_density = [round(csiutils.get_density(SapModel, k),2) for k in mat_name]

    mat_strength = []
    mod_elasticity = []
    poisson_ratio = []
    coeff_thermal_expansion = []
    for i in mat_name:
        f_,e,u,a = csiutils.get_matprop(SapModel,i)
        mat_strength.append(round(f_/1000,2))
        mod_elasticity.append(e/1000)
        poisson_ratio.append(u)
        coeff_thermal_expansion.append(a)

    mat_df = pd.DataFrame(list(zip(mat_name,mat_density,mat_strength,mod_elasticity,\
                            poisson_ratio,coeff_thermal_expansion)),columns = \
                                    ["Material_name","Density","Compressive strength\n (MPa)","Modulus of elasticity\n (MPa)",\
                                    "poisson's ratio","coeff thrml exp\n (1.0e-05/C)"])
    return mat_df

def frame_data(SapModel):
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

    beamrebar_df = pd.DataFrame(beam_df,columns = ["Frame_Name","MatPropLong",\
                        "MatPropConfine","CoverTop","CoverBot","TopLeftArea","TopRightArea","BotLeftArea","BotRightArea"])
    columnrebar_df = pd.DataFrame(column_df,columns = ["Frame_Name","MatPropLong", "MatPropConfine", "Pattern", "ConfineType", "Cover", \
                         "NumberR3Bars", "NumberR2Bars", "NumberCBars","RebarSize","TieSize", "TieSpacingLongit", "Number2DirTieBars",\
                         "Number3DirTieBars", "ToBeDesigned"])

    
    columnrebar_df = columnrebar_df.drop(['Pattern', 'ConfineType'], axis=1)
    columnrebar_df.Cover = columnrebar_df.Cover * 1000
    columnrebar_df.TieSpacingLongit = columnrebar_df.TieSpacingLongit * 1000

    # converting cover to mm
    beamrebar_df.CoverTop = beamrebar_df.CoverTop * 1000 
    beamrebar_df.CoverBot = beamrebar_df.CoverBot * 1000

    return prop_df,beamrebar_df,columnrebar_df


def framemodifier(SapModel):
    df_list = []
    prop_df = csiutils.get_frameprop(SapModel)
    for i in prop_df.Frame_Name:
        modifiers = csiutils.get_propmodifiers(SapModel,i)
        modifiers = [i for i in modifiers]
        modifiers.insert(0,i)
        df_list.append(modifiers)

    modifier_df = pd.DataFrame(df_list,columns = ["Frame_Name","Axial_mod",\
                        "Shear_22_mod","Shear_33_mod","torsion_mod","MI_22_mod","MI_33_mod","mass_mod","weight_mod"])
    return modifier_df

def main(SapModel):
    csiutils.set_units(SapModel) # set to kNmc

    utils.pretty_print(material_data(SapModel))
    input("press enter to continue to next")
    utils.pretty_print(frame_data(SapModel))
    input("press enter to continue to next")
    utils.pretty_print(framemodifier(SapModel))