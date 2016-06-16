from collections import defaultdict

CODE_SMELLS = ["HMU", "IGS", "MIM"]


# Count the number of code smells in the application output, based on the
# code smells list (see 'CODE_SMELLS' global field)
# It returns a dictionary which list the number of each code smell, and the
# global count
def count_global_cs(output):
    logcount = defaultdict(int)
    for line_output in output.splitlines():
        for code_smell in CODE_SMELLS:
            if code_smell in line_output:
                logcount[code_smell] += 1
    logcount["TOTAL"] = sum(logcount.values())
    return logcount
