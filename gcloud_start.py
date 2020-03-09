import subprocess
import sys

def run_command_print_stdout(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    print result

inst = "instance-1"
zone = "us-west2-a"
run_command_print_stdout(["gcloud", "compute", "instances", "list"])
run_command_print_stdout(["gcloud", "compute", "instances", "start", "--zone", zone, inst])
run_command_print_stdout(["gcloud", "compute", "instances", "list"])
run_command_print_stdout(["gcloud", "compute", "instances", "stop", "--zone", zone, inst])
run_command_print_stdout(["gcloud", "compute", "instances", "list"])
