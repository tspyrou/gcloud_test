import sys
import subprocess
import array as arr
import argparse
import os
import shlex
import pprint

def run_command_locally(command):
    print("command=",command)
    subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')

starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)


command = shlex.split("bash -c 'source ~/.bashrc'")
print(command)
proc = subprocess.Popen(command, stdout = subprocess.PIPE)
#for line in proc.stdout:
#  (key, _, value) = line.partition("=")
#  os.environ[key] = value
#proc.communicate()

#pprint.pprint(dict(os.environ))

run_command_locally("echo $PATH")
#run_command_locally("bash -c [source ~/.bashrc]")
command = shlex.split("bash -c 'source ~/.bashrc'")
proc = subprocess.Popen(command, stdout = subprocess.PIPE)
proc.communicate()
print (shlex.split("bash -c 'source ~/.bashrc'"))
