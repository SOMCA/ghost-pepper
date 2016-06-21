from enum import Enum


PACKAGE = ":AllowPackage:"


START_OF_INTENT = "Allowing start of Intent"


NUMBER_EVENTS = "Events injected:"


EVENT_PERCENTAGES = "Event percentages:"


DURATION = "## Network stats:"


# MonkeyEvent is a suite of Android events
class MonkeyEvent(Enum):
    TOUCH = 0
    MOTION = 1
    PINCHZOOM = 2
    TRACKBALL = 3
    ROTATION = 4
    NAV = 5
    MAJORNAV = 6
    SYSKEYS = 7
    APPSWITCH = 8
    FLIP = 9
    ANYEVENT = 10


# IntentDetails is an object to parse and get some details about intents in an
# Android application
# An intent is describe by a "cmp" key - it can also have an "act" and "cat"
# description
class IntentDetails():

    def __init__(self, output_line):
        splitted_output_line = output_line.split(" ")
        for splitted_part in splitted_output_line:
            if splitted_part.startswith("act"):
                self._act = splitted_part[4:]
            elif splitted_part.startswith("cat"):
                self._cat = splitted_part[5:-1]
            elif splitted_part.startswith("cmp"):
                self._cmp = splitted_part[4:]

    # For Set comparison
    def __eq__(self, other):
        bool_r = (self._cmp == other._cmp)
        if hasattr(self, "_act") and hasattr(other, "_act"):
            bool_r = bool_r and (self._act == other._act)
        elif hasattr(self, "_act") and not hasattr(other, "_act") or\
             not hasattr(self, "_act") and hasattr(other, "_act"):
            return False
        if hasattr(self, "_cat") and hasattr(other, "_cat"):
            bool_r = bool_r and (self._cat == other._cat)
        elif hasattr(self, "_cat") and not hasattr(other, "_cat") or\
             not hasattr(self, "_cat") and hasattr(other, "_cat"):
            return False
        return bool_r

    # For Set comparison
    def __hash__(self):
        hash_r = hash(self._cmp)
        if hasattr(self, "_act"):
            hash_r &= hash(self._act)
        if hasattr(self, "_cat"):
            hash_r &= hash(self._cat)
        return hash_r


# MonkeyDetails is an object to get all available informations about a Monkey
# run
# Those informations are obtained parsing the output of the "monkey" command
# (see parseDetails method)
class MonkeyDetails():

    def __init__(self, output):
        self._package = ""
        self._event_percentages = []
        self._intents = set()
        # self._wifi_duration = 0
        # self._mobile_duration = 0
        self._total_duration = ""
        self._number_events = ""
        self.parseDetails(output)

    def parseDetails(self, output):
        event_percentages_bool = False
        for output_line in output.splitlines():
            output_line = output_line.decode('utf-8')
            if event_percentages_bool:
                try:
                    splitted_e = output_line.split("//")[1].strip().split(":")
                    # current_position = splitted_e[0]
                    current_percentage = splitted_e[1][:-1]
                    self._event_percentages.append(current_percentage)
                    continue
                except:
                    event_percentages_bool = False
            # The following line IS NOT a 'ELIF/ELSE' statement
            if START_OF_INTENT in output_line:
                self._intents.add(IntentDetails(output_line))
            elif EVENT_PERCENTAGES in output_line:
                event_percentages_bool = True
            elif PACKAGE in output_line:
                self._package = output_line.split(PACKAGE)[1].strip()
            elif DURATION in output_line:
                splitted_e = output_line.split(DURATION)[1].strip()
                splitted_e = splitted_e.split("(")[0].strip()
                if splitted_e.startswith("elapsed time="):
                    self._total_duration = splitted_e[13:]
            elif NUMBER_EVENTS in output_line:
                self._number_events = output_line.split(NUMBER_EVENTS)[1].strip()

    def __str__(self):
        to_return = "Package %s\n" % self._package
        to_return += "Number of events injected: %s\n" % self._number_events
        to_return += "Events:\n"
        for event in MonkeyEvent:
            to_return += "\t* {0}: {1}%\n".format(
                                           event.name,
                                           self._event_percentages[event.value]
            )
        to_return += "Intents: %d called\n" % len(self._intents)
        to_return += "Duration: %sms" % self._total_duration
        return to_return
