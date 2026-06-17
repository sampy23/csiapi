import pandas as pd
import numpy as np
from collections.abc import Iterable

# import pythonnet clr-loader
import ETABSv1 as etabs
from . import utils

#=======================================================================================================================
def set_pointselection(SapModel,uniq_lab):
    point_obj = etabs.cPointObj(SapModel.PointObj)
    if isinstance(uniq_lab,str):
        ret = point_obj.SetSelected(uniq_lab,True)
        return not ret
    elif isinstance(uniq_lab,Iterable):
        ret = [point_obj.SetSelected(i, True) for i in uniq_lab]
        if sum(ret) == 0:
            return True
        else:
            return False
#=======================================================================================================================
def set_frameselection(SapModel,uniq_lab):
    frame_obj = etabs.cFrameObj(SapModel.FrameObj)
    if isinstance(uniq_lab,str):
        ret = frame_obj.SetSelected(uniq_lab,True)
        return not ret
    elif isinstance(uniq_lab,Iterable):
        ret = [frame_obj.SetSelected(i, True) for i in uniq_lab]
        if sum(ret) == 0:
            return True
        else:
            return False
#=======================================================================================================================
def set_areaselection(SapModel,uniq_lab):
    area_obj = etabs.cAreaObj(SapModel.AreaObj)
    if isinstance(uniq_lab,str):
        ret = area_obj.SetSelected(uniq_lab,True)
        if ret == 0:
            return True
        else:
            return False
    elif isinstance(uniq_lab,Iterable):
        ret = [area_obj.SetSelected(i, True) for i in uniq_lab]
        if sum(ret) == 0:
            return True
        else:
            return False

#=======================================================================================================================
class DesignConcrete:
    def __init__(self,SapModel): # Constructor - designs concrete
        if not SapModel.DesignConcrete.GetResultsAvailable():
            SapModel.DesignConcrete.StartDesign()
        else:
            print("\nWarning!!!! Showing results only for members with available design results")
        self.frame_obj = etabs.cFrameObj(SapModel.FrameObj)
        self.design_conc = etabs.cDesignConcrete(SapModel.DesignConcrete)
        self.sapmodel = SapModel

    def summary_conccolumn(self,uniq_lab):
        uniq_lab = str(uniq_lab)
        mem_type = self.member_type(uniq_lab,self.frame_obj)
        if mem_type == "Column":
            try: # for steel columns
                [ret,NumberItems,FrameName,MyOption,Location,PMMCombo,PMMArea,PMMRatio,VMajorCombo,AVMajor,VMinorCombo,\
                                        AVMinor,ErrorSummary,WarningSummary] = \
                        self.design_conc.GetSummaryResultsColumn(uniq_lab,int(),[str()],[int()],[float()],[str()],[float()],\
                                        [float()],[str()],[float()],[str()],[float()],[str()],[str()])
                
                self.design_col_df = pd.DataFrame(list(zip(FrameName,Location,PMMCombo,PMMArea,PMMRatio,\
                                                      VMajorCombo,AVMajor,VMinorCombo,AVMinor,ErrorSummary,WarningSummary)),
                                            columns = ['Unique_Name', 'Location', 'PMMCombo', 'PMMArea', 'PMMRatio',
                                                    'VMajorCombo', 'AVMajor', 'VMinorCombo','AVMinor','ErrorSummary','WarningSummary'])
                return self.design_col_df
            except IndexError:
                print("{0} is not a concrete column".format(uniq_lab))
        else:
            return None

    def summary_concbeam(self,uniq_lab):
        uniq_lab = str(uniq_lab)
        mem_type = self.member_type(uniq_lab,self.frame_obj)
        if mem_type == "Beam":
            try: # for steel beams
                [ret, NumberItems, FrameName, Location, TopCombo, TopArea, TopAreaReq,TopAreaMin, TopAreaProvided, BotCombo, \
                 BotArea, BotAreaReq, BotAreaMin, BotAreaProvided, VmajorCombo, VmajorArea, VmajorAreaReq, VmajorAreaMin,\
                 VmajorAreaProvided, TLCombo, TLArea, TTCombo, TTArea, ErrorSummary, WarningSummary] = \
                        self.design_conc.GetSummaryResultsBeam_2(uniq_lab ,int(), [str()], [float()], [str()], [float()],\
                                                [float()],[float()],[float()],[str()],[float()],[float()],\
                                                [float()],[float()],[str()],[float()],[float()],[float()],\
                                                [float()],[str()],[float()],[str()],[float()],[str()],[str()])
                
                self.design_beam_df = pd.DataFrame(list(zip(FrameName, Location, TopCombo, TopArea, TopAreaReq,TopAreaMin,\
                                                     TopAreaProvided, BotCombo,BotArea, BotAreaReq, BotAreaMin, \
                                                    BotAreaProvided, VmajorCombo, VmajorArea, VmajorAreaReq, VmajorAreaMin,\
                                                    VmajorAreaProvided, TLCombo, TLArea, TTCombo, TTArea, ErrorSummary, \
                                                    WarningSummary)),
                                    columns = ["FrameName", "Location", "TopCombo", "TopArea", "TopAreaReq",
                                               "TopAreaMin", "TopAreaProvided", "BotCombo", "BotArea", "BotAreaReq",
                                                "BotAreaMin", "BotAreaProvided", "VmajorCombo", "VmajorArea", "VmajorAreaReq",
                                                "VmajorAreaMin", "VmajorAreaProvided", "TLCombo", "TLArea", "TTCombo",
                                                "TTArea", "ErrorSummary", "WarningSummary"])
                return self.design_beam_df
            except IndexError:
                print("{0} is not a concrete beam".format(uniq_lab))
        else:
            return None
    
    def col_concdesign_forces(self,col_frame): # extracts design force for a particular column element
        """This works for both steel and concrete"""

        [ret, NumberResults, FrameName, ComboName, Station,P, V2, V3, T, M2, M3] = \
        self.sapmodel.DesignResults.DesignForces.ColumnDesignForces(str(col_frame),int(),[str()],\
                                    [str()],[float()],[float()],[float()],[float()],[float()],[float()],[float()],\
                                    etabs.eItemType.Objects)
    
        col_design_forces_df = pd.DataFrame(list(zip(FrameName, ComboName, Station,P, V2, V3, T, M2, M3)),
                            columns = ["Unique_Name", "Combo", "Station","P", "V2", "V3", "T", "M2", "M3"])
        return col_design_forces_df  

    def all_column_design_forces(self): #this will pull all the data from db, quite faster than reading line by line

        result = self.sapmodel.DatabaseTables.GetTableForDisplayArray(
            "Design Forces - Columns",
            [str()],
            str(),
            int(),
            [str()],
            int(),
            [str()]
        )

        ret = result[0]

        if ret != 0:
            raise RuntimeError("Could not retrieve column design forces table")

        # table_version = result[1]
        field_keys = list(result[1])
        # group_name = result[3]
        # num_records = result[4]
        table_data = list(result[5])

        if len(field_keys)>1:
            n_fields = len(field_keys)
        else:
            print("No field key identified, user defined headers will be used")
            field_keys = ["Story","Column","Unique_Name","Combo","Station","P","V2","V3","T","M2","M3"]
            n_fields = len(field_keys)

        # reshape 1D list to 2D
        data_array = np.array(table_data).reshape(-1, n_fields)

        df = pd.DataFrame(data_array, columns=field_keys)
        if "Frame" in df.columns:
            df.rename(columns={"Frame": "Unique_Name"}, inplace=True)

        numeric_cols = ["P", "V2", "V3", "T", "M2", "M3"]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col])

        return df

    @staticmethod
    def member_type(uniq_lab,frame_obj):
        mem_type = frame_obj.GetDesignOrientation(uniq_lab,etabs.eFrameDesignOrientation(int(),True))[1].ToString()
        return mem_type
#=======================================================================================================================
class DesignSteel:
    def __init__(self,SapModel): # Constructor - designs steel
        SapModel.DesignSteel.StartDesign()
        version = utils.version(SapModel)
        self.version = version[:2]
        self.design_steel = etabs.cDesignSteel(SapModel.DesignSteel)

    def summary_steel(self,uniq_lab):
        uniq_lab = str(uniq_lab)
        if int(self.version) > 19: # need to check for version 20 as well
            try: # for conc columns
                # Define variables for summary results
                NumberItems = int()
                FrameName = [str()]
                FrameType = [etabs.eFrameDesignOrientation.Column,etabs.eFrameDesignOrientation.Beam,\
                            etabs.eFrameDesignOrientation.Brace]
                DesignSect = [str()]
                Status = [str()]
                PMMCombo = [str()]
                PMMRatio = [float()]
                PRatio = [float()]
                MMajRatio = [float()]
                MMinRatio = [float()]
                VMajCombo = [str()]
                VMajRatio = [float()]
                VMinCombo = [str()]
                VMinRatio = [float()]

                [ret, NumberItems, FrameName, FrameType, DesignSect, Status, PMMCombo,
                                                    PMMRatio, PRatio, MMajRatio, MMinRatio, VMajCombo, VMajRatio,
                                                    VMinCombo, VMinRatio] = \
                        self.design_steel.GetSummaryResults_3(uniq_lab, NumberItems, FrameName, FrameType, DesignSect, Status, PMMCombo,
                                                    PMMRatio, PRatio, MMajRatio, MMinRatio, VMajCombo, VMajRatio,
                                                    VMinCombo, VMinRatio)
                
                design_steel_df = pd.DataFrame(list(zip(FrameName, FrameType, DesignSect, Status, PMMCombo,
                                                    PMMRatio, PRatio, MMajRatio, MMinRatio, VMajCombo, VMajRatio,
                                                    VMinCombo, VMinRatio)),
                                            columns = ["FrameName", "FrameType", "DesignSect", "Status", "PMMCombo",
                                                    "PMMRatio", "PRatio", "MMajRatio", "MMinRatio", "VMajCombo", "VMajRatio",
                                                    "VMinCombo", "VMinRatio"])
                return design_steel_df
            except IndexError:
                print("{0} is not a steel member".format(uniq_lab))
                return None
        else:
            try: 
                [ret, NumberItems, FrameType, DesignSect, Status, PMMCombo, \
                    PMMRatio, PRatio, MMajRatio,MMinRatio,VMajCombo,VMajRatio,VMinCombo,VMinRatio] = \
                        self.design_steel.GetSummaryResults_2(uniq_lab, int(), [str()], [str()], \
                                                         [str()], [str()], [float()], [float()], [float()], [float()],\
                                                        [str()], [float()], [str()], [float()],etabs.eItemType.Objects)
                
                design_steel_df = pd.DataFrame(list(zip(FrameType, \
                            DesignSect, Status, PMMCombo, PMMRatio, PRatio,MMajRatio, MMinRatio, VMajCombo, VMajRatio,\
                                     VMinCombo, VMinRatio)),
                                            columns = ['FrameType', 'DesignSect', 'Status', 'PMMCombo', \
                                                       'PMMRatio', 'PRatio', 'MMajRatio', 'MMinRatio', 'VMajCombo', \
                                                        'VMajRatio', 'VMinCombo', 'VMinRatio'])
                return design_steel_df
            except IndexError:
                print("{0} is not a steel member".format(uniq_lab))
                return None 
#=======================================================================================================================
def set_combo(SapModel,combo):
    
    #set combo selected for output
    SapModel.Results.Setup.SetComboSelectedForOutput(combo, True)

    #check if combo is selected
    ret, check = SapModel.Results.Setup.GetComboSelectedForOutput(combo, bool())
    
    return check
#=======================================================================================================================

