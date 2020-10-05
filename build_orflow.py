#!/usr/bin/env python3
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
    subprocess.run(shlex.split(command), check=True)

starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)

run_command_locally("git clone --recursive --branch openroad  git@github.com:The-OpenROAD-Project-private/OpenROAD-flow-private.git")

run_command_locally("git clone /home/zf4_projects/OpenROAD-guest/platforms/gf12.git")
#run_command_locally("git clone /home/zf4_projects/OpenROAD-guest/platforms/tsmc65lp.git")
run_command_locally("git clone https://github.com/The-OpenROAD-Project-private/private_tool_scripts.git")

os.chdir("OpenROAD-flow-private")
run_command_locally("./build_openroad.sh --latest --local --nice")
run_command_locally("bash -c 'source ./setup_env.sh'")
check_exists("openroad")
check_exists("yosys")
check_exists("TritonRoute")
