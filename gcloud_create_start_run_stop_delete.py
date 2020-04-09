def run_command_print_stdout(command):
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p1.stdout.readlines()
    return result

instance_name = "instance-auto-1"

#create an instance from a known good image
gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create instance_name --zone=us-central1-a --machine-type=c2-standard-4 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --image=openroad-ic-works-with-app-and-flow-1 --image-project=foss-fpga-tools-ext-openroad --boot-disk-size=64GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-1 --reservation-affinity=any

#start the new instance
gcloud compute start instance_name

#send it a command
gcloud compute ssh instance_name -- "ls -al .ssh"

#stop the new instance
gcloud compute start instance_name

#delete the instance
gcloud compute instances delete instance_name --delete-disks=all --quiet
