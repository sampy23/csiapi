def main():
    import os
    import importlib
    from csiapi import csiutils, utils

    SapModel = csiutils.attach()

    processors_dir = 'processors'

    modules = {}
    for file in sorted(os.listdir(processors_dir)):
        if file.endswith(".py"):
            module_name = file[:-3]
            module = importlib.import_module(f"{processors_dir}.{module_name}")
            modules[module_name] = module

    scripts = {i + 1: module for i, (name, module) in enumerate(modules.items())}

    while True:
        try:
            input_string = "Enter the following number for the desired action:\n    0  -  Exit\n"
            for i, (name, module) in enumerate(modules.items(), start=1):
                display_name = getattr(module, "NAME", name)
                description  = getattr(module, "DESCRIPTION", "")
                input_string += f"    {i}  -  {display_name}\n"
                if description:
                    input_string += f"           {description}\n"

            selection = int(input(input_string))

            if selection == 0:
                return SapModel

            if selection not in scripts:
                print("Invalid selection.")
                continue

            script = scripts[selection]

            # Guard: skip model-requiring processors if SapModel is unavailable
            if getattr(script, 'REQUIRES_MODEL', True) and SapModel is None:
                print("This processor requires an open ETABS model.")
                input("Press enter to continue")
                continue

            # -------------------------------------------------------
            # Special-cased processors (interactive back-and-forth)
            # -------------------------------------------------------
            module_file = list(modules.keys())[selection - 1]

            if module_file.startswith("1-"):
                # Checklist — 3 tables with press-enter pauses
                mat_df, frame_dfs, mod_df = script.main(SapModel)
                utils.pretty_print(mat_df)
                input("press enter to continue to next")
                utils.pretty_print(frame_dfs)
                input("press enter to continue to next")
                utils.pretty_print(mod_df)

            elif module_file.startswith("5-"):
                # Force range — show stats + histogram, then loop for bounds
                compression = script.get_compression(SapModel)
                p_min = float(compression.min())
                p_max = float(compression.max())

                print("\nGoverning compression forces (10 most critical):\n")
                print(compression.sort_values().head(10))
                print(f"\nMax axial load: {p_max:.2f} kN  |  Min axial load: {p_min:.2f} kN")

                fig = script.compression_histogram(compression)
                fig.show()

                while True:
                    print(f"\nRange: {p_min:.2f} kN  to  {p_max:.2f} kN")
                    lb = utils.input_float("Enter lower bound [kN]: ", p_min, p_max)
                    ub = utils.input_float("Enter upper bound [kN]: ", p_min, p_max)
                    if lb > ub:
                        lb, ub = ub, lb
                    result = script.main(SapModel, lb, ub)
                    print(f"\nSelected {len(result)} columns.")
                    utils.pretty_print(result)
                    if input("\nPress Enter to continue, q to exit: ").lower() == "q":
                        break

            elif module_file.startswith("8-"):
                # Reo calculator — loop until user quits
                print("\nColumn Reinforcement Ratio Calculator")
                print("Format: widthxlength_#Tdia  |  Example: 400x600_8T25")
                print("Enter 'q' to return to main menu\n")
                while True:
                    col_name = input("Column: ").strip()
                    if col_name.lower() in ("q", "quit", "exit"):
                        print("Returning to main menu...")
                        break
                    try:
                        r = script.main(SapModel, col_name)
                        print(f"  Steel Area    = {r['steel_area_mm2']} mm²")
                        print(f"  Concrete Area = {r['concrete_area_mm2']} mm²")
                        print(f"  Rebar Ratio   = {r['ratio_pct']} %\n")
                    except ValueError as e:
                        print(f"Error: {e}\n")

            # -------------------------------------------------------
            # Generic path — collect PARAMS, call main(), display result
            # -------------------------------------------------------
            else:
                params = {}
                for key, meta in getattr(script, 'PARAMS', {}).items():
                    if meta['type'] == float:
                        params[key] = utils.input_float(meta['prompt'])
                    else:
                        params[key] = meta['type'](input(meta['prompt']))

                result = script.main(SapModel, **params)

                if result is not None:
                    utils.pretty_print(result)

            input("Press enter to continue")
            print("==========================================================")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
