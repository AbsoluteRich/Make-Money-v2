import toml
import json
from os.path import exists
from Scripts import utils

print("""This is used to convert v1 saves to v2, as it uses a completely different format.
Instructions:
1. Place this file in the same folder as your 'save.json' and 'utils.py' file.
2. Type 'READY' in all caps to start. Press Enter to exit.""")

while True:
    try:
        choice = input("Awaiting input: ")
        if choice == "READY":

            if not exists("save.json"):
                utils.force_exit("Save file could not be found. Please ensure you have read the instructions.")

            print("Loading JSON...")
            with open("save.json", "r") as f:
                old_save = json.loads(f.read())

            if not old_save.get("checksum", False):
                utils.force_exit("JSON file is invalid or missing checksum.")

            print("Verifying checksum...")
            sum_of_numbers = 0  # Sum thing
            for line in old_save:
                try:
                    if old_save[line] is not True and old_save[line] is not False:
                        sum_of_numbers += old_save[line]
                except TypeError:
                    continue

            # Checks for length
            if not (old_save["checksum"][0] == len(str(sum_of_numbers))):
                utils.force_exit(f"Invalid length, "
                                 f"got '{old_save['checksum'][0]}'.")

            # Checks for valid symbol
            if not (old_save["checksum"][1] == "/" or old_save["checksum"][1] == "%"):
                utils.force_exit(f"Invalid symbol, "
                                 f"got '{old_save['checksum'][1]}'.")

            # Finally, checks if the maths works out
            if old_save["checksum"][1] == "/":
                if not (sum_of_numbers / 2 == old_save["checksum"][2]):
                    utils.force_exit(f"Invalid division, "
                                     f"got '{old_save['checksum'][2]}'.")
            elif old_save["checksum"][1] == "%":
                if not (str(sum_of_numbers / 2).split('.')[1] == str(old_save["checksum"][2])):
                    utils.force_exit(f"Invalid decimal, "
                                     f"got '{old_save['checksum'][2]}'.")
            else:
                utils.force_exit(f"Invalid symbol further into execution, got '{old_save['checksum'][1]}'.")

            print("Creating new TOML file...")
            if exists("save.toml"):
                utils.force_exit("'save.toml' already exists.")
            else:
                with open("save.toml", "x"):
                    pass

                i = 0
                # I spent two hours trying to figure out why the TOML file didn't work
                # And it fucking turns out
                # It's a problem with TOML itself, because arrays are homogeneous
                # Fuck me
                for x in old_save["checksum"]:
                    old_save["checksum"][i] = str(old_save["checksum"][i])
                    i += 1

                new_save = {
                    "coins": old_save.get("coins", 0),
                    "debt": old_save.get("debt", 0),
                    "shinies": 0,

                    "items": {
                        "auto_typer": old_save.get("autoTyper", 0),
                        "backroom_deals": old_save.get("backroomDeals", 0),
                        "weighted_chip": old_save.get("weightedChip", 0),
                    },

                    "core": {
                        "wins": 0,
                        "runs": 0,
                        "checksum": [],
                    },

                    "preferences": {
                        "patch_notes": True
                    },

                    "archived": {
                        "v1": {
                            # This probably doesn't need to be kept, but better safe than sorry
                            "checksum": old_save.get("checksum", []),
                            "runs": old_save.get("runs", 0),
                        },
                    },
                }

                with open("save.toml", "w") as f:
                    f.write(toml.dumps(new_save))

            print("Done. Check your directory to see if a file called 'save.toml' exists.")
            print("'save.json' is now useless (unless you plan on playing v1), and you may delete it.")
            input("Press Enter to exit. ")
            break

        elif choice == "":
            break

    except Exception as err:
        print("An error has occurred. See logs for more info.")
        utils.force_exit(f"{type(err).__name__}: {err}")
