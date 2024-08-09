from csiapi import csiutils,ops,utils

def select(SapModel,item):
    if ops.set_pointselection(SapModel,item):
        print(f"Points {item} selected!!")
    else:
        print("Warning!!!!Points not selected!!")

# SapModel = csiutils.attach()

def main(SapModel):
    user_input = int(input("Select single member or multiple? 1-single, 2-multiple: "))

    if user_input == 1:
        unique_label = input("Enter point unique label: ")
        csiutils.clear_selection(SapModel)
        select(SapModel, unique_label)
        csiutils.refresh(SapModel)

    elif user_input == 2:
        print("Notepad values will be used for member selection\n")
        with open(r'C:\Users\Shahabaz.muhammed\OneDrive - Surbana Jurong Private Limited\.python\etabs\support_files\points list.txt') as f:
            contents = f.read()
        contents_list = contents.split("\n")
        unique_contents_list = set(contents_list) # remove duplicates in case duplicates are present
        # Remove empty strings using set comprehension
        unique_contents_list = {item for item in unique_contents_list if item}
        csiutils.clear_selection(SapModel)
        select(SapModel,unique_contents_list)
        # [select(SapModel, i) for i in unique_contents_list]
        csiutils.refresh(SapModel)