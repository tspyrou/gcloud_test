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

instances=get_instance_names()
print("running instances=",instances," size=",len(instances))
agents = get_jenkins_agent_instance_names()
print("agents=",agents)
unique_name = create_unique_instance_name()
print(unique_name)
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




