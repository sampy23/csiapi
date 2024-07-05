import pandas as pd

def sys_to_df(list_systemobjs,columns):
    df = pd.DataFrame([list(i) for i in list_systemobjs]).transpose()
    df.columns = columns
    return df
#=======================================================================================================================
def get_object_type(enum):
    if enum == 1:
        return "Point"
    if enum == 2:
        return "Frame"
    if enum == 3:
        return "Cable" # not found
    if enum == 4:
        return "Tendon"
    if enum == 5:
        return "Area"
    if enum == 6:
        return "Solid" # not found
    if enum == 7:
        return "Link"
#=======================================================================================================================
def input_float(prompt, lower=-float("inf"), upper=float("inf"), reminder="Please enter a valid number."):
    """Accept a floating point value from the user.
        Loop until valid input has been received."""
    while True:
        try:
            value = float(input(prompt))
            if not lower <= value <= upper:
                raise ValueError
            return value
        except ValueError:
            print(reminder) 
#=======================================================================================================================
def organise(list_data):
    """Accept list of data and provide the analysis of the data as dataframe"""
    select_df = pd.DataFrame(list_data)
    select_df1 = select_df[0].value_counts(normalize=True).round(3) * 100
    select_df2 = select_df[0].value_counts()
    summary = pd.concat([select_df1,select_df2],axis=1)
    return summary
