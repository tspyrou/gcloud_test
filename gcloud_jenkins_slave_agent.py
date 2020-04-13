import subprocess
import sys
import array as arr
import gcloud_jenkins_slave_agent_utils as gu
import argparse

zone = "--zone=us-central1-c"

#print("This is the name of the script:", sys.argv[0])
#print("Number of arguments: ", len(sys.argv))
#print("The arguments are: " , str(sys.argv))

parser = argparse.ArgumentParser(description='Start jenkins agent on gcloud.')
parser.add_argument('--reuse_disk', dest='reuse_disk', action='store_true',
                    help='reuse the instance\'s disk from a previous run, same name as unique instance')
parser.add_argument('--delete_disk', dest='delete_disk', action='store_true',
                    help='delete the instance\'s disk when done, don\'t do this when planning to reuse')
parser.add_argument('unique_name', action='store',
                   help='unique gcloud instance name')
parser.add_argument('command_to_run_remotely', action='store',
                   help='command to run remotely to start jenkins\' slave.jar')
args = parser.parse_args()
unique_name = args.unique_name
delete_disk = args.delete_disk
reuse_disk = args.reuse_disk
slave_start_command = args.command_to_run_remotely
print("unique_name=", unique_name)
print("command_to_run_remotely=", slave_start_command)
print("delete_disk=", delete_disk)
print("reuse_disk=", reuse_disk)
if not gu.verify_unique_instance_name(unique_name):
    print("There is already an instance named", unique_name, "exiting.")
    exit()
if not reuse_disk:
    if not gu.verify_unique_disk_name(unique_name):
        print("There is already an instance named", unique_name, "exiting.")
        exit()

#check initial list
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_disk_names())

#create disk
print("create disk",unique_name)
cmd = "gcloud compute --project foss-fpga-tools-ext-openroad disks create " + unique_name + " "
cmd = cmd + "--size 128 " + zone + " --source-snapshot firstjenkinsagentworks-docker-clean-cronv2 --type pd-ssd"
print(cmd.split())
print(gu.run_command_locally(cmd.split()))

#create instance
print("create instance",unique_name)
cmd = "gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create " + unique_name + " "
cmd = cmd + zone + " --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append "
cmd = cmd+ "--disk=name=" + unique_name +",device-name=" + unique_name
cmd = cmd + ",mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any"
print(cmd.split())
print(gu.run_command_locally(cmd.split()))

#check if created
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_disk_names())

#wait for ssh to wake up
while True:
    retval = gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "uname", "-a"])
    if not (retval == []):
        break
    print("new instance's ssh not up yet, trying again.")

#send commands
print("running command on",unique_name)
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, zone, "--", "uname", "-a"]))
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, zone, "--", "ls", "-al"]))


#delete instance
print("deleting instance",unique_name)
print(gu.run_command_locally(["gcloud", "compute", "instances", "delete", unique_name, "--quiet"]))

#delete disk
print("deleting disk",unique_name)
print(gu.run_command_locally(["gcloud", "compute", "disks", "delete", unique_name, "--quiet"]))

#check inst and disk deleted
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_instance_names())
