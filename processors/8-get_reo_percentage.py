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


def main(SapModel):

    print("\nColumn Reinforcement Ratio Calculator")
    print("Format: widthxlength_#Tdia")
    print("Example: 400x600_8T25")
    print("Enter 'q' to return to main menu\n")

    while True:

        col_name = input("Column: ").strip()

        if col_name.lower() in ["q", "quit", "exit"]:
            print("Returning to main menu...Press Enter..\n")
            break

        try:

            ratio, steel_area, conc_area = calculate_ratio(col_name)

            print(f"\nColumn: {col_name}")
            print(f"Steel Area   = {round(steel_area,2)} mm²")
            print(f"Concrete Area= {conc_area} mm²")
            print(f"Rebar Ratio  = {ratio} %\n")

        except ValueError as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":

    SapModel = csiutils.attach()

    main(SapModel)