from lib.adb_utils import call_adb_command, get_output,\
     launch_monkey_event, call_shell_command
from lib.count import count_global_cs, rank
from lib.monkey import MonkeyDetails
from lib.progress_bar import ProgressBar
from time import sleep


APP = "my.package"


ITERATION = 10


def main():
    values = []
    bar = ProgressBar(100, 100, "PROGRESSING...")
    bar.update(0)
    bar_step = 100/ITERATION
    for i in range(ITERATION):
        log_thread = call_adb_command("log", "-c")
        log_thread.wait()
        (seed, monkey_thread) = launch_monkey_event(APP,
                                                    events="1000",
                                                    throttle="300")
        monkey_thread.wait()
        monkey_output = get_output(monkey_thread)
        print(MonkeyDetails(monkey_output))
        output = get_output(call_adb_command("log", "-d"))
        global_count = count_global_cs(output)
        values.append((seed, global_count))

        stop_thread = call_shell_command("stop", APP)
        stop_thread.wait()
        reset_thread = call_shell_command("reset", APP)
        reset_thread.wait()
        bar.update((i + 1) * bar_step)

        sleep(5)

    rank(values)


if __name__ == '__main__':
    main()
