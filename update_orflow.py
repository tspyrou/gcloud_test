#!/usr/bin/env python3
import sys
import subprocess
import array as arr
import argparse
import os
import shlex
import argparse

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
    subprocess.run(shlex.split(command))

parser = argparse.ArgumentParser(description='Update OR Flow')
parser.add_argument('--clean', action='store_true')
args = parser.parse_args()

starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)
starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)

os.environ['OPENROAD_FLOW_NO_GIT_INIT'] = 'Y'

os.chdir("OpenROAD-flow-private")
run_command_locally("git pull")

os.chdir(os.path.join(starting_dir, "gf12"))
run_command_locally("git pull")

os.chdir(os.path.join(starting_dir, "tsmc65lp"))
run_command_locally("git pull")

os.chdir(os.path.join(starting_dir, "private_tool_scripts"))
run_command_locally("git pull")

os.chdir(os.path.join(starting_dir, "OpenROAD-flow-private"))
if args.clean:
    run_command_locally("rm -rf tools/build")
run_command_locally("./build_openroad.sh --latest --local --nice")
run_command_locally("bash -c 'source ./setup_env.sh'")
check_exists("openroad")
check_exists("yosys")
check_exists("TritonRoute")

