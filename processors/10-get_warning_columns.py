NAME = "Selects Columns with warnings"
DESCRIPTION = "This selection includes columns with both delta_ns and joint shear failure"
REQUIRES_MODEL = True

import pandas as pd
from tabulate import tabulate

from csiapi import csiutils,ops

def main(SapModel):
    csiutils.clear_selection(SapModel)  #clear previous selection if any
    csiutils.run(SapModel)

    design_concrete = ops.DesignConcrete(SapModel)

    df_list = []
    frame_all = csiutils.frame_all(SapModel)
    for i in frame_all:
        df_list.append(design_concrete.summary_conccolumn(i))
    col_df = pd.concat(df_list,axis=0,join = "inner") # combine dataframe
    warning_df = col_df[col_df['WarningSummary'].str.strip().astype(bool)] # isolate which has warning which will be mostly delta_ns
    warning_df = warning_df.drop(['VMajorCombo', 'AVMajor', 'VMinorCombo', 'AVMinor'], axis=1) #inplace update

    for i in warning_df.Unique_Name:
        ops.set_frameselection(SapModel, i)

    csiutils.refresh(SapModel)
    return warning_df

if __name__ == "__main__":
    SapModel = csiutils.attach()
    main(SapModel)