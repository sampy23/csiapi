NAME = "Filters elements"
DESCRIPTION = "Selection of elements can be filtered into beams, columns, walls, floor"
REQUIRES_MODEL = True
PARAMS = {
    "obj_type": {"prompt": "Object type (Frame/Area): ", "type": str},
    "subtype":  {"prompt": "Subtype — Frame: Column/Beam/Brace  |  Area: Floor/Wall : ", "type": str}
}

from csiapi import csiutils, ops

def main(SapModel, obj_type: str, subtype: str) -> list:
    obj_type = obj_type.strip().capitalize()
    subtype  = subtype.strip().capitalize()

    df_select = csiutils.get_selection(SapModel)
    csiutils.clear_selection(SapModel)

    list_items = df_select[df_select.object_typename == obj_type].unique_label
    selected = []

    if obj_type == "Area":
        buckets = {"Floor": [], "Wall": []}
        for i in list_items:
            at = csiutils.area_type(SapModel, i)
            if at in ("Floor", "Null"):
                buckets["Floor"].append(i)
            elif at == "Wall":
                buckets["Wall"].append(i)
        for i in buckets.get(subtype, []):
            ops.set_areaselection(SapModel, i)
            selected.append(i)

    elif obj_type == "Frame":
        buckets = {"Column": [], "Beam": [], "Brace": []}
        for i in list_items:
            mt = csiutils.member_type(SapModel, i)
            if mt in buckets:
                buckets[mt].append(i)
        for i in buckets.get(subtype, []):
            ops.set_frameselection(SapModel, i)
            selected.append(i)

    csiutils.refresh(SapModel)
    return selected

if __name__ == "__main__":
    SapModel = csiutils.attach()
    ot = input("Object type (Frame/Area): ")
    st = input("Subtype: ")
    result = main(SapModel, ot, st)
    print(f"Selected {len(result)} elements")
