import sys
import subprocess
import array as arr
import argparse
import os

def run_command_locally(command):
    print("command=",command)
    subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')

starting_dir = os.getcwd()
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
print("starting_dir =",starting_dir)

run_command_locally("git clone --recursive --branch openroad https://github.com/The-OpenROAD-Project/OpenROAD-flow.git")
os.chdir("OpenROAD-flow/flow/platforms/")
run_command_locally("git clone /home/tajayi/projects/OpenROAD/alpha-release-platforms/gf14.git")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow/flow/")
run_command_locally("git clone /home/tajayi/projects/OpenROAD/alpha-release-platforms/private.git")
os.chdir(starting_dir)
os.chdir("OpenROAD-flow")
run_command_locally("./build_openroad.sh --latest --local")
#run_command_locally("env -i bash -c 'source init_env && env'")
#run_command_locally("which openroad")
#run_command_locally("which yosys")
#run_command_locally("TritonRoute")
#run_command_locally("TritonRoute14")
