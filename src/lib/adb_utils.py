from subprocess import PIPE, Popen

import os
import random

# Contains available ADB commands
ADB_COMMANDS = {
    "devices": ["devices"],
    "log": ["logcat"],
    "root": ["root"],
}

# Contains available commands to launch in an ADB SHELL
SHELL_COMMANDS = {
    "monkey": ["monkey", "-p"],
    "pkg": ["pm", "list", "packages"],
    "reset": ["pm", "clear"],
    "stop": ["am", "force-stop"],
}

# MAXIMUM NUMBER FOR 32 BITS ARCHITECTURE
MAX_32_BITS = 2**32


# Get the output of an ADB command, to display and analyse it in the program.
# Parameters:
# * output_cmd: the result of an adb or shell command
# * patterns: a regex to search usefull informations from the output
def get_output(output_cmd, *patterns):
    while True:
        # Clear the line
        try:
            line = output_cmd.stdout.readline().decode('ascii').strip()
        except Exception as e:
            print("Exception raised: {0}".format(e))
        if not line:
            break
        if not patterns or any(pattern in line for pattern in patterns):
            yield line


# Enable or disable the USB smartphone charging (USB CHARGING ONLY - not data
# transmission)
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
# This function returns the seed and the result of the command
def launch_monkey_event(package, seed=None, events="50000", throttle="500"):
    if not package:
        print("No package to run!")
        return None
    if package.startswith("package:"):
        package = package[8:]
    # Random seed if no one has been given as parameter
    if not seed:
        seed = str(random.randint(0, MAX_32_BITS))
    return (seed, call_shell_command("monkey", package,
                                     "-s", seed,
                                     "-v",
                                     "--throttle", throttle,
                                     "--pct-majornav", "40",
                                     "--pct-syskeys", "0",
                                     "--pct-touch", "30",
                                     "--pct-nav", "10",
                                     "--pct-appswitch", "0",
                                     "--pct-anyevent", "0",
                                     "--pct-motion", "20",
                                     "--kill-process-after-error",
                                     events))


# Call an ADB command via this function
# Parameters:
# * ADB_CMD: the ADB command to launch
# * CMD_ARGS: command parameters
def call_adb_command(ADB_CMD, *CMD_ARGS, shell=False, stdout=PIPE):
    if not (ADB_CMD in ADB_COMMANDS):
        print("No command %s as an adb command!" % ADB_CMD)
        return None
    JADB_CMD = " ".join(ADB_COMMANDS[ADB_CMD])
    return Popen(["adb", JADB_CMD, " ".join([s_arg for s_arg in CMD_ARGS])],
                 shell=shell, stdout=stdout)


# Call a SHELL command via this function
# Parameters:
# * SHELL_CMD: the SHELL command to launch
# * CMD_ARGS: command parameters
def call_shell_command(SHELL_CMD, *CMD_ARGS, shell=False, stdout=PIPE):
    if not (SHELL_CMD in SHELL_COMMANDS):
        print("No command %s as an adb command!" % SHELL_CMD)
        return None
    JSHELL_CMD = " ".join(SHELL_COMMANDS[SHELL_CMD])
    return Popen(["adb", "shell", JSHELL_CMD,
                  " ".join([s_arg for s_arg in CMD_ARGS])],
                 shell=shell, stdout=stdout)
