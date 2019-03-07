import subprocess
import re
import psutil

# You can watch any process in my case it was the imagent because it had a memory leak in Mac OS Sierra
PROCESS = "imagent"
THRESHOLD = 100 # MB
THRESHOLD = 2000
UNIT = "M"
UNIT = "K"

# Process list command, this will print the memory usage and the PID
COMMAND = "top -o mem -l 1 | grep imagent | awk '{print $8 \" \" $1}'"

def killProcess(pid):
  # Iterate over all running process
  for proc in psutil.process_iter():
    try:
      # Get process name & pid from process object.
      processName = proc.name()
      processPID = str(proc.pid)

      # If a match is found, then kill the process
      if (processName == PROCESS) or (processPID == pid):
        print("Trying to kill...")
        proc.kill()
        print("Killed ", processName, " with PID ", processPID)
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as error:
      print("Error: ", error)
      return False

  return False

# This runs until no more matches are found
def runUntilKilled(pid):
  res = killProcess(pid)
  if not res:
    print("No process to kill")
    return 

  # Loop the processes and kill matches
  while res:
    res = killProcess(pid)

  print("Process killed.")

# Execute process list command
output = subprocess.check_output(['bash','-c', COMMAND])
output = str(output).split(' ')

# subprocess.check_output(['bash','-c', 'open .'])

memory = output[0]
pid = output[1]

mem_regex = "(\d)"
unit_regex = "([KMB])"

# Memory info
mem = re.findall(mem_regex, memory)
mem = int(''.join(str(e) for e in mem))

# Unit M, K, B (Megabytes, kilobytes, bytes)
unit = re.findall(unit_regex, memory)[0]

# PID
pid = ''.join(re.findall(mem_regex, pid))

# print(mem, unit, pid)
print("==========RUNNING=============")
# If an undesired process is found, we get rid of it
if unit == UNIT and mem >= THRESHOLD:
  print("Found mem. leak process! Killing " + pid)
  runUntilKilled(pid)
else:
  print("No mem. leak processes found")
