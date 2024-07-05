import pandas as pd

from csiapi import csiutils,ops

SapModel = csiutils.attach()
csiutils.clear_selection(SapModel)  #clear previous selection if any
csiutils.run(SapModel)
design_concrete = ops.DesignConcrete(SapModel)

df_list = []
frame_all = csiutils.frame_all(SapModel)
for i in frame_all:
    df_list.append(design_concrete.summary_conccolumn(i))
col_df = pd.concat(df_list,axis=0,join = "inner") # combine dataframe
warning_df = col_df[col_df['WarningSummary'].str.strip().astype(bool)] # isolate which has warning which will be mostly delta_ns

print(col_df)
for i in warning_df.Unique_Name:  #select locally buckled members
    ops.set_frameselection(SapModel,i)

csiutils.refresh(SapModel)