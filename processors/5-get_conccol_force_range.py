NAME = "Select Column by Axial force"
DESCRIPTION = "Programs runs and designs the model and then allow user to select columns in particular range."
REQUIRES_MODEL = True
# No PARAMS — this processor is special-cased in main.py because it needs to
# show statistics and a histogram before the user can enter meaningful bounds.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure

from csiapi import csiutils, ops

def get_compression(SapModel) -> pd.Series:
    """Run analysis, design, and return per-column minimum axial force (compression)."""
    csiutils.run(SapModel)
    csiutils.set_units(SapModel)

    design_concrete = ops.DesignConcrete(SapModel)
    df = design_concrete.all_column_design_forces()
    df["P"] = pd.to_numeric(df["P"], errors="coerce")
    return df.groupby("Unique_Name")["P"].min()

def compression_histogram(compression: pd.Series) -> matplotlib.figure.Figure:
    """Return a matplotlib Figure of the axial load distribution histogram."""
    fig, ax = plt.subplots()
    ax.hist(compression.dropna(), bins=15)
    ax.set_title("Column Axial Load Distribution")
    ax.set_xlabel("Axial Force (kN)")
    ax.set_ylabel("Number of Columns")
    return fig

def main(SapModel, lower_bound: float, upper_bound: float) -> pd.DataFrame:
    """Select columns whose controlling compression is within [lower_bound, upper_bound].
    Returns a DataFrame of the selected columns and their axial forces."""
    compression = get_compression(SapModel)

    selected = compression[
        (compression >= lower_bound) & (compression <= upper_bound)
    ]
    selected_cols = list(set(selected.index.tolist()))

    SapModel.SelectObj.ClearSelection()
    ops.set_frameselection(SapModel, selected_cols)

    return selected.reset_index().rename(columns={"Unique_Name": "Column", "P": "Min_P_kN"})

if __name__ == "__main__":
    import sys
    from csiapi import utils

    SapModel = csiutils.attach()
    compression = get_compression(SapModel)

    p_min = float(compression.min())
    p_max = float(compression.max())

    print("\nGoverning compression forces (10 most critical):\n")
    print(compression.sort_values().head(10))
    print(f"\nMaximum axial load: {p_max:.2f} kN")
    print(f"Minimum axial load: {p_min:.2f} kN")

    compression_histogram(compression).show()

    while True:
        print(f"\nRange: {p_min:.2f} kN to {p_max:.2f} kN")
        lb = utils.input_float("Enter lower bound [kN]: ", p_min, p_max)
        ub = utils.input_float("Enter upper bound [kN]: ", p_min, p_max)
        if lb > ub:
            lb, ub = ub, lb
        result = main(SapModel, lb, ub)
        print(f"\nSelected {len(result)} columns.")
        utils.pretty_print(result)
        if input("\nPress Enter to continue, q to exit: ").lower() == "q":
            break
