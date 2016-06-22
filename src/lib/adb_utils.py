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
    "simiasque": ["am", "broadcast", "-a",
                  "org.thisisafactory.simiasque.SET_OVERLAY", "--ez",
                  "enable"],
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
            line = output_cmd.stdout.readline().decode('utf-8').strip()
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

    return (seed, call_command("monkey",
                               package,
                               "-s",
                               seed,
                               "-v", "-v", "-v",
                               "--throttle", throttle,
                               "--pct-majornav", "0",
                               "--pct-syskeys", "0",
                               "--pct-touch", "15",
                               "--pct-nav", "15",
                               "--pct-appswitch", "50",
                               "--pct-anyevent", "0",
                               "--pct-motion", "20",
                               "--kill-process-after-error",
                               events))


# Enable or disable SIMIASQUE - SIMIASQUE is a tool to disable top-to-bottom
# interations using Monkey
# Parameter:
# * boolean: True to enable SIMIASQUE, else False
def enable_simiasque(boolean=True):
    return call_command("simiasque", "true") if boolean\
           else call_command("simiasque", "false")


# Call an ADB/SHELL command via this function
# Parameters:
# * CMD: the ADB/SHELL command to launch
# * CMD_ARGS: command parameters
def call_command(CMD, *CMD_ARGS, shell=False, stdout=PIPE):
    if not (CMD in ADB_COMMANDS) and not (CMD in SHELL_COMMANDS):
        print("No command %s as an adb/shell command!" % CMD)
        return None
    command_list = ["adb"]
    if CMD in SHELL_COMMANDS:
        command_list.append("shell")
    J_CMD = ADB_COMMANDS[CMD] if (CMD in ADB_COMMANDS) else SHELL_COMMANDS[CMD]
    command_list += J_CMD + list(CMD_ARGS)
    return Popen(command_list,
                 shell=shell, stdout=stdout, stderr=PIPE)
