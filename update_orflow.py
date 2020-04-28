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
starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)

os.chdir("OpenROAD-flow")
run_command_locally("git pull")
os.chdir("flow/platforms/gf14")
run_command_locally("git pull")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow/flow/private")
run_command_locally("git pull")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow/tools/OpenROAD")
run_command_locally("git pull")
run_command_locally("git submodule update --init --recursive")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow/tools/yosys")
run_command_locally("git pull")
run_command_locally("git submodule update --init --recursive")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow/tools/TritonRoute")
run_command_locally("git pull")
run_command_locally("git submodule update --init --recursive")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow/tools/TritonRoute14")
run_command_locally("git pull")
run_command_locally("git submodule update --init --recursive")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow")
run_command_locally("rm -rf tools/build")
run_command_locally("./build_openroad.sh --latest --local")
run_command_locally("source ./setup_env.sh")
run_command_locally("which openroad")
run_command_locally("which yosys")
run_command_locally("TritonRoute")
run_command_locally("TritonRoute14")
