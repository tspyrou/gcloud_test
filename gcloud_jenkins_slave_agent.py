import sys
import subprocess
import array as arr
import argparse
import os
print("path to script=",os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
print("current path=",sys.path)
import gcloud_jenkins_slave_agent_utils as gu

# Run jenkins in central region for reduced cost and higher cpu allocation
zone = "--zone=us-central1-c"

# Parse and check arguments
parser = argparse.ArgumentParser(description='Start jenkins agent on gcloud.')
parser.add_argument('--reuse_disk', dest='reuse_disk', action='store_true',
                    help='reuse the instance\'s disk from a previous run, same name as unique instance')
parser.add_argument('unique_name', action='store',
                   help='unique gcloud instance name')
parser.add_argument('command_to_run_remotely', action='store',
                   help='command to run remotely to start jenkins\' slave.jar')
args = parser.parse_args()
unique_name = args.unique_name
reuse_disk = args.reuse_disk
slave_start_command = args.command_to_run_remotely
print("unique_name=", unique_name)
print("command_to_run_remotely=", slave_start_command)
print("reuse_disk=", reuse_disk)

# Report initial list of instances and disks to log
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_instance_names())

# Cleanup if there are zombie instances or disks for some reason
if not gu.verify_unique_instance_name(unique_name):
    print("There is already an instance named", unique_name, "deleting it.")
    print(gu.delete_instance(unique_name, zone))
    
if not reuse_disk:
    if not gu.verify_unique_disk_name(unique_name):
        print("There is already a disk named", unique_name, "deleting it.")
        print(gu.delete_disk(unique_name, zone))

# Create or reuse the disk
create_missing_disk = False
if (not unique_name in gu.get_disk_names()) and reuse_disk:
    print("Warning: --reuse_disk requested but disk", unique_name, "does not exist. Ignoring option and creating a new disk.")
    create_missing_disk = True
if create_missing_disk or (not reuse_disk):
    #create disk
    print("create disk",unique_name)
    cmd = "gcloud compute --project foss-fpga-tools-ext-openroad disks create " + unique_name + " "
    cmd = cmd + "--size 128 " + zone + " --source-snapshot firstjenkinsagentworks-docker-clean-cronv2 --type pd-ssd"
    print(cmd.split())
    print(gu.run_command_locally(cmd.split()))
else:
    print("Reusing disk", unique_name)

#create instance, do not auto delete the disk so it can be reused if desired
print("create instance",unique_name)
print(gu.create_instance(unique_name, zone))
              
#check if created
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_disk_names())

#wait for ssh to wake up
retries_left = 50
while True:
    retval = gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, zone, "--", "uname", "-a"])
    if not (retval == []):
        print(retval)
        break
    retries_left -= 1
    print("new instance's ssh not up yet, trying again. retries_left", retries_left)
    if retries_left <= 0:
        print("exhausted shh retries, skipping command")
        break

if (retries_left > 0):
    #send command
    print("running", slave_start_command, "on",unique_name)
    cmd = ["gcloud", "beta", "compute", "ssh",  unique_name, zone, "--","-tT -v"]
    for elem in slave_start_command.split():
        cmd.append(elem)
    print(gu.run_command_locally(cmd))


#delete instance
print("deleting instance",unique_name)
print(gu.delete_instance(unique_name, zone))

#delete disk
if not reuse_disk:
    print("deleting disk",unique_name)
    print(gu.delete_disk(unique_name, zone))
if reuse_disk:
    if not unique_name in gu.get_disk_names():
        print("ERROR: disk", unique_name, " does not exist for re-use")
    
#check inst and disk deleted
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_instance_names())
