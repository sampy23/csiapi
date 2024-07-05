from csiapi import csiutils,ops

with open(r'C:\Users\Shahabaz.muhammed\OneDrive - Surbana Jurong Private Limited\.python\etabs\support_files\member labels list.txt') as f:
    contents = f.read()

contents_list = contents.split("\n")
unique_contents_list = set(contents_list) #unique list

SapModel = csiutils.attach()
csiutils.clear_selection(SapModel)
ops.set_frameselection(SapModel,unique_contents_list)
csiutils.refresh(SapModel)
