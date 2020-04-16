import subprocess
import sys
import array as arr

def run_command_locally(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    print("command=",command)
    #p1 = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    return result

def get_disk_names():
    disk_list_gcloud_retval = run_command_locally(["gcloud", "compute", "disks", "list"])
    disk_list_gcloud_retval = disk_list_gcloud_retval[1: len(disk_list_gcloud_retval)]
    disk_list = []
    for desk_retval in disk_list_gcloud_retval:
        desk = desk_retval.split()[0]
        disk_list.append(desk.decode('utf-8'))
    disk_list.sort()
    return disk_list

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

def verify_unique_instance_name(name):
    agents = get_instance_names()
    found = name in agents
    if found:
        return False
    return True

def verify_unique_disk_name(name):
    disks = get_disk_names()
    found = name in disks
    if found:
        return False
    return True

def delete_disk(unique_name):
    retval = run_command_locally(["gcloud", "compute", "disks", "delete", unique_name, "--quiet"])
    if unique_name in get_disk_names():
        print("ERROR: disk", unique_name, " not deleted correctly")
    return retval

def create_instance(unique_name, zone):
    #create instance, do not auto delete the disk so it can be reused if desired
    cmd = "gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create " + unique_name + " "
    cmd = cmd + zone + " --machine-type=c2-standard-16 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append "
    cmd = cmd+ "--disk=name=" + unique_name +",device-name=" + unique_name
    cmd = cmd + ",mode=rw,boot=yes,auto-delete=no --reservation-affinity=any"
    retval = run_command_locally(cmd.split())
    return retval

def delete_instance(unique_name):
    print(run_command_locally(["gcloud", "compute", "instances", "delete", unique_name, "--quiet"]))
    if unique_name in get_instance_names():
        print("ERROR: instance", unique_name, " not deleted correctly")
