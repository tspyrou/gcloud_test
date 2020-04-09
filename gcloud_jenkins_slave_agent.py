import subprocess
import sys
import array as arr

def run_command_locally(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    return result

def get_instance_names():
    instance_list_gcloud_retval = run_command_locally(["gcloud", "compute", "instances", "list"])
    instance_list_gcloud_retval = instance_list_gcloud_retval[1: len(instance_list_gcloud_retval)]
    instance_list = []
    for inst_retval in instance_list_gcloud_retval:
        inst = inst_retval.split()[0]
        instance_list.append(inst.decode('utf-8'))
    instance_list.sort()
    return instance_list

def get_jenkins_agent_prefix():
    return "openroad-public-jenkins-agent"

def get_jenkins_agent_instance_names():
    prefix = get_jenkins_agent_prefix()
    instance_names = get_instance_names()
    agents = []
    for inst in instance_names:
        if inst[0:len(prefix)] == prefix:
            agents.append(inst)
    agents.sort()
    return agents

def create_unique_instance_name():
    prefix = get_jenkins_agent_prefix()
    agents = get_jenkins_agent_instance_names()
    current_try_num = 1
    while True:
        current_try_name = prefix + "-" + str(current_try_num)
        if not current_try_name in agents:
            break
        current_try_num += 1
    return current_try_name    

def run_command_remotely(user, host, keyfile, command):
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

unique_name = create_unique_instance_name()
print("creating new instance ",unique_name)

# create disk
#gcloud compute --project "foss-fpga-tools-ext-openroad" disks create "unique_name" --size "256" --zone "us-central1-c" --source-snapshot "firstjenkinsagentworks-docker-clean-cronv2" --type "pd-ssd"
print(["gcloud", "compute", "--project", "foss-fpga-tools-ext-openroad", "disks", "create", unique_name, "--size", "256", "--zone", "us-central1-c", "--source-snapshot", "firstjenkinsagentworks-docker-clean-cronv2", "--type", "pd-ssd"])



#create instance
#gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create unique_name --zone=us-central1-c --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=unique_name,device-name=unique_name,mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any
print(["gcloud beta compute", "--project=foss-fpga-tools-ext-openroad", "instances", "create", unique_name, "--zone=us-central1-c", "--machine-type=c2-standard-16", "--subnet=default", "--network-tier=PREMIUM", "--maintenance-policy=MIGRATE", "--service-account=281156998478-compute@developer.gserviceaccount.com", "--scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append", "--disk=name=", unique_name, "device-name=unique_name,mode=rw,boot=yes,auto-delete=yes", "--reservation-affinity=any"])


#send command
#gcloud compute ssh unique_name -- uname -a
print(["gcloud", "compute", "ssh", unique_name, "--", "uname", "-a"])
#delete instance
#gcloud compute instances delete unique_name --delete-disks=all --quiet
print(["gcloud", "compute", "instance", "delete",  unique_name, "--delete-disks=all", "--quiet"])

