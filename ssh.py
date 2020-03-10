import subprocess
import sys


def run_command_remotely_ssh(user, host, keyfile, command):
    print user, host, keyfile, command
    user_host=user+"@"+host
    ssh = subprocess.Popen(["ssh", "-i", keyfile, user_host, command],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    print result
    return result

result = run_command_remotely_ssh("tspyrou", "34.94.233.163", "~/.ssh/gcloud", "uname -a")

#if result == []:
#    error = ssh.stderr.readlines()
#    print >>sys.stderr, "ERROR: %s" % error
#else:
#    print result
