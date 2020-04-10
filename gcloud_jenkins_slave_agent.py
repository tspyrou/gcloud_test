import subprocess
import sys
import array as arr
import gcloud_jenkins_slave_agent_utils as gu

print(gu.run_command_locally(["ls", "-al"]))

unique_name = gu.create_unique_instance_name()

#gcloud compute --project "foss-fpga-tools-ext-openroad" disks create "instance-1" --size "128" --zone "us-central1-c" --source-snapshot "firstjenkinsagentworks-docker-clean-cronv2" --type "pd-ssd"
cmd = "gcloud compute --project foss-fpga-tools-ext-openroad disks create " + unique_name + " "
cmd = cmd + "--size 128 --zone us-central1-c --source-snapshot firstjenkinsagentworks-docker-clean-cronv2 --type pd-ssd"
print(cmd.split())
print(gu.run_command_locally(cmd.split()))

#gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create instance-1 --zone=us-central1-c --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=instance-1,device-name=instance-1,mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any
cmd = "gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create " + unique_name + " "
cmd = cmd + "--zone=us-central1-c --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append "
cmd = cmd+ "--disk=name=" + unique_name +",device-name=" + unique_name
cmd = cmd + ",mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any"
print(cmd.split())
print(gu.run_command_locally(cmd.split()))

print(gu.run_command_locally(["gcloud", "compute", "disks", "list"]))
print(gu.run_command_locally(["gcloud", "compute", "instances", "list"]))

#send command
#gcloud beta compute ssh openroad-public-jenkins-agent-1 -- "uname -a"
print("running command on",unique_name)
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "uname", "-a"]))
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "ls", "-al"]))
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "touch", "t.t"]))
print(gu.run_command_locally(["gcloud", "beta", "compute", "ssh",  unique_name, "--", "whoami"]))

#delete instance
#gcloud compute instances delete unique_name --delete-disks=all --quiet
print("deleting instance",unique_name)
print(gu.run_command_locally(["gcloud", "compute", "instances", "delete",  unique_name, "--quiet"]))
print("deleting disk",unique_name)
print(gu.run_command_locally(["gcloud", "compute", "disks", "delete",  unique_name, "--quiet"]))
print(gu.run_command_locally(["gcloud", "compute", "instances", "list"]))
print(gu.run_command_locally(["gcloud", "compute", "disks", "list"]))


