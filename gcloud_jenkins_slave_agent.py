import subprocess
import sys
import array as arr

def get_external_ip_from_list_return_value(instance_list):
    inst_data = instance_list[1].split()
    external_ip = inst_data[4]
    return external_ip

def get_instance_names(instance_list_gcloud_retval):
    instance_list_gcloud_retval = instance_list_gcloud_retval[1: len(instance_list_gcloud_retval)]
    instance_list = []
    for inst_retval in instance_list_gcloud_retval:
        inst = inst_retval.split()[0]
        instance_list.append(inst.decode('utf-8'))
    return instance_list

def run_command_print_stdout(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    return result

def run_command_remotely_ssh(user, host, keyfile, command):
    user_host=user+"@"+host
    ssh = subprocess.Popen(["ssh", "-oStrictHostKeyChecking=no", "-i", keyfile, user_host, command],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        return error
    return result

retval_instances = run_command_print_stdout(["gcloud", "compute", "instances", "list"])
instances=get_instance_names(retval_instances)
print("running instances=",instances)

#gcloud compute --project "foss-fpga-tools-ext-openroad" disks create "instance-1" --size "128" --zone "us-west2-a" --source-snapshot "firstjenkinsagentworks" --type "pd-ssd"

#gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create instance-1 --zone=us-west2-a --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=instance-1,device-name=instance-1,mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any


#result = run_command_remotely_ssh("tspyrou", ip_add, "~/.ssh/gcloud", "uname -a")
#print "remote result=", result
#run_command_print_stdout(["gcloud", "compute", "instances", "stop", "--zone", zone, inst])
#print run_command_print_stdout(["gcloud", "compute", "instances", "list"])

# should have done this with google cloud run - for ephemeral things.
# Google cloud build, docker images etc, has docker container registry, private containers too
# Make machines ephemeral. For example run jenkins server at UCSD but executors in the cloud.
# Make deleting and stopping machines the same. Only stop is you want to keep data on the machine.




