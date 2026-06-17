NAME = "Column Reinforcement Ratio"
DESCRIPTION = "Checks reinforcement percentage of columns"
REQUIRES_MODEL = False

import math
from csiapi import csiutils


def calculate_ratio(col_name):

    col_name = col_name.lower().replace("-", "_")

    try:
        col_size, rebar = col_name.split("_")

        width, length = col_size.split("x")
        rebar_num, rebar_dia = rebar.split("t")

        width = int(width)
        length = int(length)
        rebar_num = int(rebar_num)
        rebar_dia = int(rebar_dia)

    except Exception:
        raise ValueError(
            "Format must be: widthxlength_#Tdia  (Example: 400x600_8T25)"
        )

    concrete_area = width * length

    rebar_area = math.pi * rebar_dia ** 2 / 4

    total_rebar_area = rebar_num * rebar_area

    ratio = round(total_rebar_area * 100 / concrete_area, 2)

    return ratio, total_rebar_area, concrete_area


def main(SapModel, column_string: str) -> dict:
    """Calculate rebar ratio for a single column string.
    Returns dict with keys: column, steel_area, concrete_area, ratio."""
    ratio, steel_area, conc_area = calculate_ratio(column_string)
    return {
        "column": column_string,
        "steel_area_mm2": round(steel_area, 2),
        "concrete_area_mm2": conc_area,
        "ratio_pct": ratio,
    }

if __name__ == "__main__":
    print("\nColumn Reinforcement Ratio Calculator")
    print("Format: widthxlength_#Tdia  |  Example: 400x600_8T25")
    print("Enter 'q' to exit\n")
    while True:
        col_name = input("Column: ").strip()
        if col_name.lower() in ("q", "quit", "exit"):
            break
        try:
            r = main(None, col_name)
            print(f"  Steel Area    = {r['steel_area_mm2']} mm²")
            print(f"  Concrete Area = {r['concrete_area_mm2']} mm²")
            print(f"  Rebar Ratio   = {r['ratio_pct']} %\n")
        except ValueError as e:
            print(f"Error: {e}\n")