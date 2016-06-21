from lib.adb_utils import call_command, get_output,\
     launch_monkey_event, enable_simiasque
from lib.count import count_global_cs, rank
from lib.monkey import MonkeyDetails
from lib.progress_bar import ProgressBar

from argparse import ArgumentParser
from collections import defaultdict
from time import sleep


APP = "my.package"


ITERATION = 10


def main():

    # Parse program arguments
    args = ArgumentParser(description="Tool to create automatically \
                          Monkey-based scenarios, \
                          ranked based code smells counting")
    args.add_argument("-e", "--events", help="Number of events to process",
                      default="100000")
    args.add_argument("-t", "--throttle", help="Delay between each event",
                      default="0")
    args = args.parse_args()

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
                                                    events="10000",
                                                    throttle="0")
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

    for seed in set_top_3:
        print("SEED %s" % seed)
        print(seed_to_details[seed])
        print("#"*40)


if __name__ == '__main__':
    main()
