import subprocess
import sys
import array as arr

def get_external_ip_from_list_return_value(retval):
    inst_data = retval[1].split()
    external_ip = inst_data[4]
    return external_ip

def run_command_print_stdout(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    return result

def run_command_remotely_ssh(user, host, keyfile, command):
    user_host=user+"@"+host
    ssh = subprocess.Popen(["ssh", "-oStrictHostKeyChecking=no", "-i", keyfile, user_host, command],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        return error
    return result

inst = "instance-1"
zone = "us-west2-a"
print run_command_print_stdout(["gcloud", "compute", "instances", "list"])
print run_command_print_stdout(["gcloud", "compute", "instances", "start", "--zone", zone, inst])
retval_started = run_command_print_stdout(["gcloud", "compute", "instances", "list"])
ip_add = get_external_ip_from_list_return_value(retval_started)
result = run_command_remotely_ssh("tspyrou", ip_add, "~/.ssh/gcloud", "uname -a")
print "remote result=", result
run_command_print_stdout(["gcloud", "compute", "instances", "stop", "--zone", zone, inst])
print run_command_print_stdout(["gcloud", "compute", "instances", "list"])

# should have done this with google cloud run - for ephemeral things.
# Google cloud build, docker images etc, has docker container registry, private containers too
# Make machines ephemeral. For example run jenkins server at UCSD but executors in the cloud.
# Make deleting and stopping machines the same. Only stop is you want to keep data on the machine.



