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
def save(SapModel):
    ret = SapModel.File.Save(str())
    return ret
#=======================================================================================================================
def get_units(SapModel):
    units = SapModel.GetPresentUnits_2(etabs.eForce.kN ,etabs.eLength.m  ,etabs.eTemperature.C)
    units = units[1:]
    units = [i.ToString() for i in units]
    return units
def set_units(SapModel):
    ret = SapModel.SetPresentUnits_2(etabs.eForce.kN ,etabs.eLength.m  ,etabs.eTemperature.C)
    return ret
#=======================================================================================================================
def get_density(SapModel,material):
    density = SapModel.PropMaterial.GetWeightAndMass(material, float(), float())[1] 
    return density
#=======================================================================================================================
def get_names(SapModel):
    [ret, mat_num, mater_iter] = SapModel.PropMaterial.GetNameList(int(), str())
    return mater_iter
#=======================================================================================================================
def get_matprop(SapModel,material):
    """Returns Fc', Modulus of elasticity, Poisson's ratio, Coefficient of thermal expansion"""
    [ret,f_,IsLightweight,fcsfactor,SSType,SSHysType,\
    StrainAtfc,StrainUltimate,FinalSlope,FrictionAngle,DilatationalAngle] = SapModel.PropMaterial.\
                                                            GetOConcrete_1(material, float(), bool(), float(), int(),\
                                                            int(), float(), float(), float(), float(), float())
    if ret: # for steel prop
        [ret,f_,Fu,EFy,EFu,SSType,SSHysType,StrainAtHardening,\
                        StrainUltimate,FinalSlope,UseCaltransSSDefaults] = SapModel.PropMaterial.\
                                                            GetORebar_1(material, float(), float(), float(), float(),\
                                                            int(), int(), float(), float(), float(), bool())
        
    [ret,e,u,a,g] = SapModel.PropMaterial.GetMPIsotropic(material, float(), float(), float(), float())
    return f_,e,u,a
#=======================================================================================================================
def get_frameprop(SapModel):
    [ret,NumberNames,MyName,PropType,t3,t2,tf,tw,t2b,tfb] = \
                    SapModel.PropFrame.GetAllFrameProperties(int(),[str()],[etabs.eFramePropType.Rectangular],\
                                                            [float()],[float()],[float()],[float()],[float()],[float()])
    
    prop_df = pd.DataFrame(list(zip(MyName,PropType,t2,t3,tf,tw,t2b,tfb)),columns = \
                                            ["Frame_Name","PropType","width","depth","flange_thk",\
                                                                            "web_thk","bot_flang_wid","bot_flang_thk"])
    return prop_df

def get_beamrebar(SapModel,frame_name):
    [ret,MatPropLong,MatPropConfine,CoverTop,CoverBot,TopLeftArea,TopRightArea,BotLeftArea,BotRightArea]\
          = SapModel.PropFrame.GetRebarBeam(frame_name,str(),str(),float(),float(),float(),float(),float(),float())
    
    return [ret,MatPropLong,MatPropConfine,CoverTop,CoverBot,TopLeftArea,TopRightArea,BotLeftArea,BotRightArea]

def get_colrebar(SapModel,frame_name):
    [ret,MatPropLong, MatPropConfine, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize,\
      TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned] \
        = SapModel.PropFrame.GetRebarColumn(frame_name,str(),str(),int(),int(),float(),int(),int(),int(),str(),str(),\
                                            float(),int(),int(),bool())
    return [ret,MatPropLong, MatPropConfine, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize,\
      TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned]
#=======================================================================================================================
def get_propmodifiers(SapModel,frame_name):
    [ret, modifiers] = SapModel.PropFrame.GetModifiers(frame_name,[float()])
    return modifiers
