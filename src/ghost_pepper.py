from lib.adb_utils import call_command, get_output,\
     launch_monkey_event, enable_simiasque
from lib.count import count_global_cs, rank
from lib.monkey import MonkeyDetails
from lib.progress_bar import ProgressBar

from argparse import ArgumentParser
from collections import defaultdict
from time import sleep

import threading

APP = "my.package"

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

    values = []
    bar = ProgressBar(100, 100, "PROGRESSING...")
    bar.update(0)
    bar_step = 100/ITERATION
    seed_to_details = defaultdict()
    enable_simiasque(True)

    for i in range(ITERATION):
        log_thread = call_command("log", "-c")
        log_thread.wait()
        (seed, monkey_thread) = launch_monkey_event(APP,
                                                    events=args.events,
                                                    throttle=args.throttle)
        monkey_output, _ = monkey_thread.communicate()
        output = get_output(call_command("log", "-d"))
        global_count = count_global_cs(output)
        values.append((seed, global_count))
        seed_to_details[seed] = MonkeyDetails(monkey_output)

        stop_thread = call_command("stop", APP)
        stop_thread.wait()
        reset_thread = call_command("reset", APP)
        reset_thread.wait()
        bar.update((i + 1) * bar_step)

        sleep(5)

    enable_simiasque(False)
    set_top_3 = rank(values)

    if args.only_one:
        print("The best seed is %s" % set_top_3["TOTAL"][0])
    elif args.verbose:
        for seed in set_top_3:
            print("SEED %s" % seed)
            print(seed_to_details[seed])
            print("#"*40)


if __name__ == '__main__':
    main()
