from datetime import datetime
from sys import exit


# https://breadcrumbscollector.tech/stop-naming-your-python-modules-utils/


def log(message):
    try:
        with open("logs.txt", "x"):
            pass
    except FileExistsError:
        pass

    with open("logs.txt", "a") as f:
        print(f"[{datetime.now()}] {message}", file=f)


def force_exit(error, prompt=True):
    if prompt is True:
        input(f"{error} ")
    log(f"ForceExit: {error}")
    exit(error)


def sinput(prompt="", sep=" ", end=">>", mode=None):
    match mode:  # The proper solution is to make each individual mode a boolean, but I'm stupid
        case "compare":
            return input(f"{prompt}{sep}{end}").casefold().strip()
        case "interrupt":
            if prompt == "":
                prompt = "Enter"
            return input(f"Press {prompt} to continue.{sep}{end}")
        case _:
            return input(f"{prompt}{sep}{end}")


def positive_input(prompt):
    # Todo: This should be a function inside sinput
    if prompt.casefold().strip() in ["true", "1", "t", "y", "yes", "yeah", "yup", "certainly", "uh-huh"]:
        return True
    else:
        return False
