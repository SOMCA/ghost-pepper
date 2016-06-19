from enum import Enum


PACKAGE = ":AllowPackage:"


START_OF_INTENT = "Allowing start of Intent"


EVENT_PERCENTAGES = "Event percentages"


DURATION = "## Network stats:"


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


class IntentDetails():

    def __init__(self, output_line):
        splitted_output_line = output_line.split(" ")
        for splitted_part in splitted_output_line:
            splitted_part = splitted_part.strip()
            if splitted_part.startswith("act"):
                self._act = splitted_part[4:]
            elif splitted_part.startswith("cat"):
                self._cat = splitted_part[5:-1]
            elif splitted_part.startswith("cmp"):
                self._cmp = splitted_part[4:]

    # For Set comparison
    def __eq__(self, other):
        return (self._act == other._act) and\
               (self._cat == other._cat) and\
               (self._cmp == other._cmp)

    # For Set comparison
    def __hash__(self):
        return (hash(self._act) & hash(self._cat) & hash(self._cmp))


class MonkeyDetails():

    def __init__(self, output):
        self._package = ""
        self._event_percentages = []
        self._intents = set()
        # self._wifi_duration = 0
        # self._mobile_duration = 0
        self._total_duration = ""
        self.parseDetails(output)

    def parseDetails(self, output):
        event_percentages_bool = False
        for output_line in output:
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

    def __str__(self):
        to_return = "Package %s\n" % self._package
        to_return += "Events:\n"
        for event in MonkeyEvent:
            to_return += "\t* {0}: {1}%\n".format(
                                           event.name,
                                           self._event_percentages[event.value]
            )
        to_return += "Intents: %d called\n" % len(self._intents)
        to_return += "Duration: %sms" % self._total_duration
        return to_return