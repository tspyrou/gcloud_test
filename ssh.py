import subprocess
import sys


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

result = run_command_remotely_ssh("tspyrou", "34.94.27.137", "~/.ssh/gcloud", "uname -a")
print result
