import subprocess
import sys
import array as arr
import gcloud_jenkins_slave_agent_utils as gu

unique_name = gu.create_unique_instance_name()

#check initial list
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_disk_names())

#create disk
print("create disk",unique_name)
cmd = "gcloud compute --project foss-fpga-tools-ext-openroad disks create " + unique_name + " "
cmd = cmd + "--size 128 --zone us-central1-c --source-snapshot firstjenkinsagentworks-docker-clean-cronv2 --type pd-ssd"
print(cmd.split())
print(gu.run_command_locally(cmd.split()))

#create instance
print("create instance",unique_name)
cmd = "gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create " + unique_name + " "
cmd = cmd + "--zone=us-central1-c --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append "
cmd = cmd+ "--disk=name=" + unique_name +",device-name=" + unique_name
cmd = cmd + ",mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any"
print(cmd.split())
print(gu.run_command_locally(cmd.split()))

#check if created
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_disk_names())

#send commands
print("running command on",unique_name)
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "uname", "-a"]))
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "ls", "-al"]))


#delete instance
print("deleting instance",unique_name)
print(gu.run_command_locally(["gcloud", "compute", "instances", "delete", unique_name, "--quiet"]))

#delete disk
print("deleting disk",unique_name)
print(gu.run_command_locally(["gcloud", "compute", "disks", "delete", unique_name, "--quiet"]))

#check inst and disk deleted
print("disk_names",gu.get_disk_names())
print("instance_names",gu.get_instance_names())
