import subprocess
import sys

def run_command_print_stdout(command):
    print command
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    if result == []:
        error = p1.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        print result

run_command_print_stdout(["ls", "-l"])
