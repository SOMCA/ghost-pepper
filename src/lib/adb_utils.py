from subprocess import PIPE, Popen

import os
import random

# Contains available ADB commands
ADB_COMMANDS = {
    "devices": ["devices"],
    "log": ["logcat", "-d"],
    "logc": ["logcat", "-c"],
    "root": ["root"],
}

# Contains available commands to launch in an ADB SHELL
SHELL_COMMANDS = {
    "monkey": ["monkey", "-p"],
    "pkg": ["pm", "list", "packages"],
}

# MAXIMUM NUMBER FOR 32 BITS ARCHITECTURE
MAX_32_BITS = 2**32


# Get the output of an ADB command, to display and analyse it in the program
# The parameter 'patterns' can contains a regex to search usefull informations
# in the output - default is None.
def get_output(output_cmd, *patterns):
    while True:
        # Clear the line
        line = output_cmd.stdout.readline().decode('ascii').strip()
        if not line:
            break
        if not patterns or any(pattern in line for pattern in patterns):
            yield line


# Enable or disable the USB smartphone charging only
def enable_usb_charging(enable=True):
    status_charge = "1" if enable else "0"
    command = "adb shell \"echo %s >\
        /sys/class/power_supply/usb/device/charge\"" % status_charge
    os.system(command)


# Launch a monkey event on the smartphone
# This event can be parametrized:
# * package : the package name of the tested application
# * seed    : the seed of the monkey test to run
# * events  : the number of events
# * throttle: a fixed delay between events
def launch_monkey_event(package, seed=None, events="50000", throttle="500"):
    if not package:
        print("No package to run!")
        return None
    if not seed:
        seed = str(random.randint(0, MAX_32_BITS))
    # '--pct-majornav' option to 0 -> disable navigation actions
    return call_shell_command("monkey", package, "-s", seed, "-v", events,
                              "--throttle", throttle, "--pct-majornav", "0")


# Call an ADB command via this function
def call_adb_command(ADB_CMD, *CMD_ARGS, shell=False, stdout=PIPE):
    if not (ADB_CMD in ADB_COMMANDS):
        print("No command %s as an adb command!" % ADB_CMD)
        return None
    return Popen(["adb", ADB_CMD, " ".join([s_arg for s_arg in CMD_ARGS])],
                 shell=shell, stdout=stdout)


# Call a SHELL command via this function
def call_shell_command(SHELL_CMD, *CMD_ARGS, shell=False, stdout=PIPE):
    if not (SHELL_CMD in SHELL_COMMANDS):
        print("No command %s as an adb command!" % SHELL_CMD)
        return None
    JSHELL_CMD = " ".join(SHELL_COMMANDS[SHELL_CMD])
    return Popen(["adb", "shell", JSHELL_CMD,
                  " ".join([s_arg for s_arg in CMD_ARGS])],
                 shell=shell, stdout=stdout)
