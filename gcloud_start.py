import subprocess
import sys
import array as arr

def get_external_ip_from_start_return_value(retval):
    print "ext=", retval
    inst_data = retval[1].split()
    external_ip = inst_data[4]
    print external_ip
    return external_ip

def run_command_print_stdout(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    return result

inst = "instance-1"
zone = "us-west2-a"
print run_command_print_stdout(["gcloud", "compute", "instances", "list"])
print run_command_print_stdout(["gcloud", "compute", "instances", "start", "--zone", zone, inst])
retval_started = run_command_print_stdout(["gcloud", "compute", "instances", "list"])
ip_add = get_external_ip_from_start_return_value(retval_started)
print ip_add
run_command_print_stdout(["gcloud", "compute", "instances", "stop", "--zone", zone, inst])
print run_command_print_stdout(["gcloud", "compute", "instances", "list"])
