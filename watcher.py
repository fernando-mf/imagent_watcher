import re
import subprocess
from enum import Enum

import psutil


class Unit(Enum):
    KB = "K"
    MB = "M"
    GB = "G"
    TB = "T"


class Multiplier(Enum):
    KB = 1
    MB = 1000 * KB
    GB = 1000 * MB
    TB = 1000 * GB


# You can watch any process in my case it was the imagent because it had a memory leak in Mac OS Sierra
PROCESS = "imagent"
UNIT = Unit.MB
THRESHOLD = 100 * Multiplier[UNIT.name].value  # Normalize size unit to KB

# Process list command, this will print "$memory_usage $PID $proces_name"
COMMAND = "top -o mem -l 1 | grep imagent | awk '{print $8 \" \" $1 \" \" $2}'"


def kill_process(pid_):
    process = psutil.Process(pid_)
    if process.name() == PROCESS:
        process.kill()
        print("Killed. pid={} pname={}".format(pid_, process.name()))
    return True


# This runs until no more matches are found
def run_until_killed(pid_):
    res = kill_process(pid_)
    if not res:
        print("No process to kill")
        return


# Execute process list command
output = subprocess.check_output(['bash', '-c', COMMAND])
output = str(output).split(' ')

# subprocess.check_output(['bash','-c', 'open .'])

memory = output[0]
pid = output[1]
pname = re.findall("(.*)\\\\n", output[2])[0]

mem_regex = "(\d)"
unit_regex = "([KMGTB])"

# Unit T, G, M, K, B (Megabytes, kilobytes, bytes)
unit = re.findall(unit_regex, memory)[0]
unit = Unit(unit)

# Memory info
mem = re.findall(mem_regex, memory)
mem = int(''.join(str(e) for e in mem))
match unit:  # Normalize size unit to KB
    case UNIT.MB:
        mem *= Multiplier.MB.value
    case UNIT.GB:
        mem *= Multiplier.GB.value
    case UNIT.TB:
        mem *= Multiplier.TB.value

# PID
pid = int(''.join(re.findall(mem_regex, pid)))

# print(mem, unit, pid)
print("==========RUNNING=============")
# If an undesired process is found, we get rid of it
if mem >= THRESHOLD:
    print("Found memory-leaking process! Killing process \"{}\" (pid={} mem={}{}>{}{}).".format(
        pname, pid,
        mem / Multiplier[unit.name].value, unit.name,
        THRESHOLD / Multiplier[UNIT.name].value, UNIT.name
    ))
    run_until_killed(pid)
else:
    print("No memory-leaking processes found.")
