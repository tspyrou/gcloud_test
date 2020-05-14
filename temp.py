import sys
import subprocess
import array as arr
import argparse
import os
import shlex

def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

def check_exists(pgm):
    if which(pgm) == None:
        print(pgm, "not on path")


def run_command_locally(command):
    print("command=",command)
    subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode('utf-8')

starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)
run_command_locally("bash -c 'source ~/.bashrc'")
check_exists("openroad")
check_exists("yosys")
check_exists("TritonRoute")
check_exists("TritonRoute14")