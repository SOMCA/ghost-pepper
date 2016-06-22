from lib.adb_utils import call_command, get_output,\
     launch_monkey_event, enable_simiasque
from lib.count import count_global_cs, rank
from lib.monkey import MonkeyDetails
from lib.progress_bar import ProgressBar

from argparse import ArgumentParser
from collections import defaultdict
from time import sleep

import threading


# Python class to launch a thread to parse logcat and to stop it when it is
# possible
class LogcatProcessThread(threading.Thread):

    def __init__(self):
        super(LogcatProcessThread, self).__init__()
        self._stop = threading.Event()
        self._data = []
        t = threading.Thread(target=self.run_process)
        t.start()

    # Method to know if the thread is stopped or not
    def is_stopped(self):
        self._stop.is_set()

    # Parse logcat during it entire lifetime
    def run_process(self):
        # While the stop event hasn't been set...
        while not self.is_stopped():
            for line in get_output(call_command("log", "-d")):
                self._data.append(line.strip())
            clear_log_thread = call_command("log", "-c")
            clear_log_thread.wait()
            # Wait for 3 seconds before parsing the next state
            sleep(3)

    # Stop the thread
    def stop(self):
        self._stop.set()


# This function run an instance, which is ITERATIONS launch of Monkey
# This function returns the top 3 of seeds for each code smell
def run_an_instance(args):

    values = []
    bar = ProgressBar(100, 100, "PROGRESSING...")
    bar.update(0)
    bar_step = 100/args.iterations
    seed_to_details = defaultdict()
    enable_simiasque(True)
    APP = args.package

    for i in range(args.iterations):
        # Go on crazy Monkey!
        log_thread = call_command("log", "-c")
        log_thread.wait()
        # Launch get_logcat and get logs as output
        logcat_object = LogcatProcessThread()
        (seed, monkey_thread) = launch_monkey_event(APP,
                                                    events=args.events,
                                                    throttle=args.throttle)
        # Get the status of the current output from monkey_thread
        monkey_output, _ = monkey_thread.communicate()
        # If Monkey is done, set the event to True
        logcat_object.stop()
        output = logcat_object._data
        # Parse things...
        global_count = count_global_cs(output)
        values.append((seed, global_count))
        seed_to_details[seed] = MonkeyDetails(monkey_output)

        stop_thread = call_command("stop", APP)
        stop_thread.wait()
        reset_thread = call_command("reset", APP)
        reset_thread.wait()
        bar.update((i + 1) * bar_step)

        # Delete the logcat object
        del logcat_object

        sleep(5)

    enable_simiasque(False)
    return (rank(values), seed_to_details)


def main():

    # Parse program arguments
    args = ArgumentParser(description="Tool to create automatically \
                          Monkey-based scenarios, \
                          ranked based code smells counting")
    args.add_argument("-e", "--events", help="Number of events to process",
                      default="100000")
    args.add_argument("-i", "--iterations", help="Number of iterations",
                      type=int, default=50)
    args.add_argument("-o", "--only_one", help="Return only one seed - the \
                      greatest number of code smells called",
                      action="store_true")
    args.add_argument("-p", "--package", help="The Android package to run",
                      required=True)
    args.add_argument("-t", "--throttle", help="Delay between each event",
                      default="0")
    args.add_argument("-v", "--verbose", help="Verbose mod for top seeds",
                      action="store_true")
    args = args.parse_args()

    # Run INSTANCES instances, where each instance contains differents values
    # of events percentage
    ((set_top_3, top_seed), seed_to_details) = run_an_instance(args)

    if args.only_one:
        print("The best seed is {0}".format(top_seed))
    elif args.verbose:
        for seed in set_top_3:
            print("SEED %s" % seed)
            print(seed_to_details[seed])
            print("#"*40)

if __name__ == '__main__':
    main()
