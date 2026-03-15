NAME = "Delta_ns calculation for a column"
DESCRIPTION = "The code calculates delta ns for a column and list it first 50 rows in descending order about minor direction"
REQUIRES_MODEL = True

import pandas as pd
import numpy as np
import ETABSv1 as etabs
from csiapi import csiutils,ops,utils


def main (SapModel):

    memb_UN = input("Enter the Unique name of column: ")

    #Column design
    design_concrete = ops.DesignConcrete(SapModel)
    df = design_concrete.col_concdesign_forces(memb_UN)
        
    # delta_ns calculation
    b_dns = 0.8

    section_name = csiutils.get_section(SapModel,memb_UN)
    material_name = csiutils.get_prop_material(SapModel,section_name)
    fc_ = csiutils.get_matprop(SapModel,material_name)[0]/1000 #MPa
    [cover,circle_bars,bars_along_3,bars_along_2, bar_dia] = csiutils.get_colrebar(SapModel,section_name)[5:10]

    prop_df = csiutils.get_frameprop(SapModel)
    t2 = prop_df[prop_df.Frame_Name == section_name].width.item() * 1000 #mm
    t3 = prop_df[prop_df.Frame_Name == section_name].depth.item() * 1000 #mm
    b = t2 #assuming 2 axis along width
    h = t3 #assuming  3 axis along depth
    cover = cover*1000 #mm
    bar_dia = int(bar_dia)

    As = np.pi * bar_dia**2 / 4


    y_minor = b/2 - cover - bar_dia/2
    Is_minor = 2 * bars_along_2 * As * y_minor**2

    y_major = h/2 - cover - bar_dia/2
    Is_major = 2 * bars_along_3 * As * y_major**2

    df["Ec"] = 4700 * np.sqrt(fc_)   # MPa
    Es = 200000      

    df_target = df[df["Unique_Name"] == memb_UN].copy() #Use .copy() to avoid SettingWithCopyWarning


    df_target["Ig2"]  = h*b**3/12   # bending about local 2 axis
    df_target["Ig3"]  = b*h**3/12   # bending about local 3 axis


    # function to get ratio of moments
    group_cols = ["Unique_Name", "Combo"]


    def get_ratio(g, moment_col):
        first = g.loc[g["Station"].idxmin(), moment_col]
        last  = g.loc[g["Station"].idxmax(), moment_col]

        return first/last if abs(first) < abs(last) else last/first

    ratio_m2 = (
        df_target.groupby(group_cols)[["Station","M2"]]
        .apply(lambda g: get_ratio(g, "M2"))
        .rename("M2_ratio")
    )

    ratio_m3 = (
        df_target.groupby(group_cols)[["Station","M3"]]
        .apply(lambda g: get_ratio(g, "M3"))
        .rename("M3_ratio")
    )

    df_target = df_target.merge(ratio_m2, on=group_cols)
    df_target = df_target.merge(ratio_m3, on=group_cols)

    df_target["Cm2"] = np.maximum(0.4, 0.6 + 0.4*df_target["M2_ratio"])
    df_target["Cm3"] = np.maximum(0.4, 0.6 + 0.4*df_target["M3_ratio"])
    df_target["Lu"] = df_target.groupby(["Combo"])["Station"].transform("max")
    df_target["Lu"] = pd.to_numeric(df_target["Lu"], errors='coerce') # Converts 'N/A' to NaN
    df_target["Lu"] *= 1000


    df_target["EIeff2"] = (0.2*df_target["Ec"]*df_target["Ig2"] + Es*Is_minor)/(1+b_dns)
    df_target["EIeff3"] = (0.2*df_target["Ec"]*df_target["Ig3"] + Es*Is_major)/(1+b_dns)


    df_target["Pcr2"] = (np.pi**2 * df_target["EIeff2"]) / (df_target["Lu"]**2)/1000
    df_target["Pcr3"] = (np.pi**2 * df_target["EIeff3"]) / (df_target["Lu"]**2)/1000


    # df_target = df_target.drop(columns=['V2',"V3"])
    df_target["delta_ns_2"] = df_target["Cm2"] / (1 - df_target["P"].abs()/(0.75*df_target["Pcr2"]))
    df_target["delta_ns_3"] = df_target["Cm3"] / (1 - df_target["P"].abs()/(0.75*df_target["Pcr3"]))


    df_print = df_target.sort_values("delta_ns_2",ascending=False).head(20)
    utils.pretty_print(df_print)

if __name__ == "__main__":
    SapModel = csiutils.attach()
    main(SapModel)