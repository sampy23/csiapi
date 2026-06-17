NAME = "Selects points by Unique name"
DESCRIPTION = "Selection of points can be done by single input or from list in notepad"
REQUIRES_MODEL = True
PARAMS = {
    "labels": {"prompt": "Enter point label(s) comma-separated (or 'file' for points list.txt): ", "type": str}
}

from csiapi import csiutils, ops

def main(SapModel, labels: str) -> bool:
    if labels.strip().lower() == "file":
        with open(r'support_files\points list.txt') as f:
            contents = f.read()
        label_set = {item for item in contents.split("\n") if item.strip()}
    else:
        label_set = {l.strip() for l in labels.split(",") if l.strip()}

    csiutils.clear_selection(SapModel)
    result = ops.set_pointselection(SapModel, label_set)
    csiutils.refresh(SapModel)
    return result

if __name__ == "__main__":
    SapModel = csiutils.attach()
    user_input = input("Enter point label(s) comma-separated (or 'file' for points list.txt): ")
    print("Selected:", main(SapModel, user_input))
