from Scripts import utils, requesting
from Scripts.utils import sinput
from dotenv import load_dotenv
import os
import toml
from json import dumps as format_dict
import random

# ================================= EXTERNAL VARIABLES =================================
print("Setting variables...")
load_dotenv()
debug_server = requesting.Webhook(os.getenv("DEBUG_SERVER"))
spam_server = requesting.Webhook(os.getenv("SPAM_SERVER"))
cool_number = int(os.getenv("DIVISION_FACTOR"))
versioning = requesting.Changelog("test1", "2.0.0", "nightly")

print("Getting version info...")
version = versioning.get_version()
changelog = versioning.get_changelog()

# ================================= FILE SHIT =================================
print("Reading save file...")

try:
    with open("save.toml", "r") as f_in:
        save_file = toml.loads(f_in.read())
    del f_in
except FileNotFoundError:
    utils.force_exit("Save file not found. Please read the release notes for more instructions.")


def read_save(section, subkey):
    section = save_file.get(section, None)
    if section is None:
        return None
    return section.get(subkey, None)


def create_checkstring():
    # Use tried and tested algorithms like MD5 to generate a checksum? Who do you think I am, someone smart?
    checkstring = []
    sum_of_numbers = 0

    # Creating the sum
    for x in save_file:
        if x in ["coins", "shinies", "debt"]:
            sum_of_numbers += int(save_file[x])

    for x in save_file["items"]:
        sum_of_numbers += int(save_file["items"][x])

    checkstring.append(len(str(sum_of_numbers)))
    divided = sum_of_numbers / cool_number

    if divided.is_integer():
        # Number is divisible
        checkstring.append(0)
        checkstring.append(int(random.randint(0, 99_999_999)))  # Make it look like there's some important info
    else:
        # Number is not divisible
        checkstring.append(1)
        divided = str(divided).split(".")
        divided = divided[1]
        checkstring.append(int(divided))

    # Why does the join method also need a homogeneous list
    return ";".join(str(num) for num in checkstring)


def check_checkstring():
    pass  # This should read the save file, then create a checkstring from the sum of its numbers
    # and compare it with whatever's in the save file
    # return generated_checkstring == checkstring


def update_save():
    save_file["core"]["checkstring"] = create_checkstring()

    with open("save.toml", "w") as f_out:
        f_out.write(toml.dumps(save_file))
    del f_out


# ================================= FUNCTIONS =================================
def clear():
    clearable = read_save("flags", "disable_cmd")

    if (clearable is None) or (clearable is False):
        if os.name == "nt":  # Windows
            os.system("cls")
        else:  # For macOS and Linux (os.name would be posix)
            os.system("clear")
    else:
        print("\n")


# ================================= MISC. VARIABLES =================================
class Item:
    def __init__(self, description, price, nature=None, stock=0):
        self.description = description
        self.price = price
        self.nature = True if nature is not None else False  # If nature has ANY value, returns True
        self.stock = stock

    def __repr__(self):
        string = f"{self.description}\n"

        if self.nature is True:
            if self.stock >= 1:
                string += "Unlocked"
            else:
                string += f"Locked for ${self.price}"
        else:
            string += f"Costs ${self.price} for one, you have {self.stock}"

        return string


# ================================= CORE VARIABLES =================================
commands = {
    "help": "This message",
    "dev": "Send a message to my personal Discord server",
    "debug": "",
    "work": "",
    "shop": "",
    "settings": "",
}

items = {
    "testing item": Item("This is a cool item!", "1 million"),
    "Item 2": Item("Item 2", 50),
    "Recombobulator Piece": Item("Collect all 3 to reform the universe", 10000)
}


# ================================= MAIN PROGRAM =================================
def startup():
    clear()

    print(f"{version['name']} ({versioning.release})")
    print("(c) AbsoluteRich. All rights reserved.")

    if read_save("preferences", "patch_notes") is True:
        if version["notes"]:
            print("Patch notes:\n" + changelog)
            sinput(mode="interrupt")

        if save_file["core"]["runs"] > 1:
            print("Tip: To stop seeing patch notes, toggle it off in the settings.")

    save_file["core"]["runs"] += 1
    update_save()

    if versioning.release == "nightly":
        # Nightly
        if not versioning.up_to_date():
            print("A nightly build is no longer available. Please upgrade to the latest beta or stable release.")
    else:
        # Stable + beta
        if not versioning.up_to_date():
            print(f"Game is out of date. Please upgrade to the latest {versioning.release} release.")

    print("Type 'help' for a list of commands.\n")


def main():
    choice = sinput(prompt="", sep="", mode="compare")

    match choice:
        case "help":
            for x in sorted(commands):
                print(f"- {x}: {commands[x]}")
            print("Commands are not case sensitive.")

        case "dev":
            choice = sinput("Why?")
            spam_server.send(choice)

        case "debug":
            if read_save("flags", "dev_mode"):
                choice = sinput("(print/send/error/exit/edit)", mode="compare")

                match choice:
                    case "print":
                        print(format_dict(save_file, indent=4))

                    case "send":
                        choice = sinput("Debug or spam?", mode="compare")

                        match choice:
                            case "debug":
                                debug_server.send(sinput(prompt="", sep=""))

                            case "spam":
                                spam_server.send(sinput(prompt="", sep=""))

                    case "error":
                        raise Exception("This is an error.")

                    case "exit":
                        utils.force_exit("This is a force exit.")

                    case "edit":
                        choice = int(sinput(sep=""))
                        save_file["coins"] = choice

            else:
                utils.force_exit(error="Not so fast", prompt=False)

        case "work":
            save_file["coins"] += random.randint(50, 250)

        case "shop":
            for x in items:
                print(f"{x}\n{items[x]}\n")

        case "settings":
            pass  # Todo


def handle_error(error):
    error = f"{type(error).__name__}: {error}"
    debug_server.send(error)
    utils.log(error)
    del error


# ================================= MAIN LOOP =================================
if __name__ == "__main__":
    try:
        startup()

        while True:
            try:
                print(f"Coins: {save_file['coins']}")
                print(f"Shinies: {save_file['shinies']}")
                main()
                update_save()
                print("\n")

            except Exception as e:  # It's stupid that I need to copy these twice
                print("An error has occurred. See logs for more info.\n")
                handle_error(e)
                del e

    except Exception as e:  # but it's the only obvious solution as I need to do this for both functions
        print("An error has occurred. See logs for more info.\n")
        handle_error(e)
        del e
