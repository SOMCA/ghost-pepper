from collections import defaultdict

CODE_SMELLS = ["HMU", "IGS", "MIM"]


LINE_PREZ = "TOP 3 FOR"


C_LINE_PREZ = len(LINE_PREZ)


# Count the number of code smells in the application output, based on the
# code smells list (see 'CODE_SMELLS' global field)
# 'output' is a generator which contains the output of an ADB/SHELL command
# It returns a dictionary which list the number of each code smell, and the
# global count
def count_global_cs(output):
    logcount = defaultdict(int)
    count_line = 0
    for line_output in output:
        count_line += 1
        for code_smell in CODE_SMELLS:
            if code_smell in line_output:
                logcount[code_smell] += 1
    logcount["TOTAL"] = sum(logcount.values())
    return logcount


def rank(values):
    top_3 = defaultdict(list)
    for cod_sm in CODE_SMELLS:
        top_3[cod_sm] = list(sorted(values, key=lambda t: t[1][cod_sm],
                             reverse=True))[0:3]
    top_3["TOTAL"] = list(sorted(values, key=lambda t: t[1]["TOTAL"],
                          reverse=True))[0:3]
    for (key, values) in top_3.items():
        print("%s %s" % (LINE_PREZ, key))
        print("#" * (C_LINE_PREZ + len(key) + 1))
        for value in values:
            print("\tSEED %s - %d calls" % (value[0], value[1][key]))
