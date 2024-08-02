from csiapi import csiutils,ops,utils

def select(item):
    csiutils.clear_selection(SapModel)
    if ops.set_frameselection(SapModel,item):
        print("Members selected!!")
    else:
        print("Members not selected!!")
    csiutils.refresh(SapModel)

SapModel = csiutils.attach()

user_input = int(input("Select single member or multiple? 1-single, 2-multiple: "))

if user_input == 1:
    unique_label = input("Enter member unique label: ")
    select(unique_label)

elif user_input == 2:
    print("Notepad values will be used for member selection")
    with open(r'C:\Users\Shahabaz.muhammed\OneDrive - Surbana Jurong Private Limited\.python\etabs\support_files\member list.txt') as f:
        contents = f.read()
    contents_list = contents.split("\n")
    unique_contents_list = set(contents_list) # remove duplicates in case duplicates are present
    # Remove empty strings using set comprehension
    unique_contents_list = {item for item in unique_contents_list if item}
    select(unique_contents_list)

