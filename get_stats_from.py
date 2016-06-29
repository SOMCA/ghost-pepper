import argparse
import csv
import re
import statistics

from glob import glob

VOLTAGE_NEXUS_4 = 3.8


def get_stats_from(files_names,
                   files_content,
                   only_mean=False,
                   globalst=False):
    stats_by_file = {}
    for i in files_content:
        file_content = files_content[i]
        if not globalst:
            file_name = files_names[i - 1]
            print("FILE {0} ({1} measures)"
                  .format(len(file_content), file_name))
            print("\t*MEAN : %.2fmA"
                  % statistics.mean(file_content))
            if only_mean:
                print("\t*MEDIAN : %.2fmA"
                      % statistics.median(file_content))
                try:
                    print("\t*MOST TYPICAL VALUE : %.2fmA"
                          % statistics.mode(file_content))
                except:
                    print("\t2 most typical values!")
                print("\t*STANDARD DEVIATION : %.2fmA"
                      % statistics.stdev(file_content))
                print("\t*VARIANCE : %.2f"
                      % statistics.variance(file_content))
        stats_by_file[i] = statistics.mean(file_content)
    return stats_by_file


def get_global_stats(files_content, only_mean=False):
    data = [files_content[f] for f in files_content]
    print("GLOBAL STATS")
    print("############")
    print("\t*GLOBAL MEAN : %.2fmA"
          % statistics.mean(data))
    if not only_mean:
        print("\t*GLOBAL MEDIAN : %.2fmA"
              % statistics.median(data))
        try:
            print("\t*GLOBAL MOST TYPICAL VALUE : %.2fmA"
                  % statistics.mode(data))
        except:
            print("\t2 most typical values!")
        print("\t*GLOBAL STANDARD DEVIATION : %.2fmA"
              % statistics.stdev(data))
        print("\t*GLOBAL VARIANCE : %.2f"
              % statistics.variance(data))


def main():
    parser = argparse.ArgumentParser(
        description="Get stats from Powertool output")
    parser.add_argument('-d', '--deterministic', type=int,
                        help="Remove the n first values from data")
    parser.add_argument('-g', '--globalst', action="store_true", default=False,
                        help="Get only global values")
    parser.add_argument('-m', '--mean', action="store_true", default=False,
                        help="Only compute the mean for each test")
    parser.add_argument('-p', '--path', type=str, default=None, required=True,
                        help="specify path to your directories")
    args = parser.parse_args()

    mean_by_file = {}
    installation_times = []
    times = []

    with open("%s/%s" % (args.path, "installation_time.txt"), "r") as i_file:
        for line in i_file:
            line = line.strip()
            if line:
                installation_times.append(float(line.split(":")[1]
                                                    .strip()))

    csv_files = [x for x in glob(args.path + "/*") if ".csv" in x]

    for csv_file_pointer in csv_files:
        with open(csv_file_pointer, "r") as csv_content:
            current_number_file = float(csv_file_pointer.split(".csv")[0]
                                                        .strip()
                                                        .split("_")[1])
            csv_reader = csv.reader(csv_content)
            flow = [row for row in csv_reader]
            current_time = [float(row[0]) for row in flow
                            if not (re.match("^\d+?\.\d+?$", row[1]) is None)]
            # Get the index of the installation time for the current project
            installation_time_index = current_time\
                .index(installation_times[current_number_file])
            # Get the `installation_time_index` first time values
            current_time = current_time[installation_time_index:]
            # Get the `installation_time_index` first measures
            measures = [float(row[1]) for i, row in enumerate(flow)
                        if not (re.match("^\d+?\.\d+?$", row[1]) is None) and
                        i >= installation_time_index]
            mean_by_file[int(csv_file_pointer
                             .split('.csv')[0][-2::]
                             .replace("_", ""))] = measures
            times.append(current_time[-1] - current_time[0])

    stats_by_file = get_stats_from(csv_files,
                                   mean_by_file,
                                   args.mean,
                                   args.globalst)

    get_global_stats(mean_by_file, args.mean)

    energies = []

    for i in stats_by_file:
        average_energy_for_i =\
            VOLTAGE_NEXUS_4 * (stats_by_file[i] / 1000) * times[i - 1]
        energies.append(average_energy_for_i)

    print("\t*GLOBAL MEAN POWER: %.2fJ" %
          round(sum(energies)/len(energies), 2))

    print("\t*GLOBAL MEAN INSTALLATION TIME: %.3fs" %
          round(sum(installation_times)/len(installation_times), 2))

    print("\t*GLOBAL MEAN EXECUTION TIME: %.2fs" %
          round(sum(times)/len(times), 2))

if __name__ == '__main__':
    main()
