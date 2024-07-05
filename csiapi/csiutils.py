import os
import pandas as pd

# import pythonnet clr-loader
import ETABSv1 as etabs
from .  import utils

#=======================================================================================================================
def attach():
    # Initialize ETABS object
    helper = etabs.cHelper(etabs.Helper())
    etabs_object = etabs.cOAPI(helper.GetObject("CSI.ETABS.API.ETABSObject"))
    SapModel = etabs_object.SapModel
    file_path = SapModel.GetModelFilename()
    file_name_ext = os.path.basename(file_path)
    print(f"Attached file is {file_name_ext}")
    return SapModel
#=======================================================================================================================
def run(SapModel):
    ret = SapModel.Analyze.RunAnalysis()
    return ret
#=======================================================================================================================
def version(SapModel):
    [ret,version,version_num] = SapModel.GetVersion(str(),float())
    return version
#=======================================================================================================================
def get_name(SapModel):
    """Returns: 'File name', 'extension', 'file path'"""
    try:
        file_path = SapModel.GetModelFilename() # absolute file path
    except:
        # logger.error("Model not found. Model might be closed or not captured by the software")
        return None
    else:
        if file_path: # if etabs opened with no specifice models
            old__name_ext = os.path.basename(file_path)
            old_name,ext = os.path.splitext(old__name_ext)
            return old_name,ext,file_path
#=======================================================================================================================
def clear_selection(SapModel):
    ret = SapModel.SelectObj.ClearSelection()
    return ret
#=======================================================================================================================
def get_selection(SapModel):
    select = etabs.cSelect(SapModel.SelectObj)
    [ret,NumberItems,ObjectType,ObjectName] = select.GetSelected(int(),[int()],[str()])
    df = utils.sys_to_df([ObjectType,ObjectName],columns = ["object_type","unique_label"])
    df["object_typename"] = [utils.get_object_type(i) for i in df.object_type]
    df = df[["object_type","object_typename","unique_label"]] #rearranging column order
    return df
#=======================================================================================================================
def refresh(SapModel):
    ret = SapModel.View.RefreshView()
    return ret
#=======================================================================================================================
def member_type(SapModel,uniq_lab):
    frame_obj = etabs.cFrameObj(SapModel.FrameObj)
    mem_type = frame_obj.GetDesignOrientation(uniq_lab,etabs.eFrameDesignOrientation(int(),True))[1].ToString()
    return mem_type
def area_type(SapModel,uniq_lab):
    area_obj = etabs.cAreaObj(SapModel.AreaObj)
    area_type = area_obj.GetDesignOrientation(uniq_lab,etabs.eAreaDesignOrientation(int(),True))[1].ToString()
    return area_type
#=======================================================================================================================
def get_section(SapModel,uniq_lab):
    frame_obj = etabs.cFrameObj(SapModel.FrameObj)
    [ret,obj_name,s_auto] = frame_obj.GetSection(uniq_lab,str(),str())
    return obj_name
#=======================================================================================================================
def frame_all(SapModel):
    frameobj = etabs.cFrameObj(SapModel.FrameObj)
    [ret,total,frame_iter] = frameobj.GetNameList(int(),str())
    return list(frame_iter)
#=======================================================================================================================
