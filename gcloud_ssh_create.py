
# google cloud all instances should be ephemeral things.
# Google cloud build, docker images etc, has docker container registry, private containers too
# Make machines ephemeral. For example run jenkins server at UCSD but executors in the cloud.
# Make deleting and stopping machines the same. Only stop is you want to keep data on the machine.
# save snapshots to disks to save for restart  later

    #Always delete instances as soon as the current job is done.
    #Google will complain if there are stopped unused instances.
    #Make a disk snapshot from the boot disk of the instance to save.


    gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create instance-1 --zone=us-west2-a --machine-type=c2-standard-8 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=openroad-ic-tom-1,device-name=openroad-ic-tom-1,mode=rw,boot=yes --reservation-affinity=any# make a snapshot from a manually configured instance to save
    #gcloud compute disks snapshot instance-1 --project=foss-fpga-tools-ext-openroad --snapshot-names=snapshot-4 --zone=us-west2-a --storage-location=us
    
    # make a disk from a snapshot
    #gcloud compute --project "foss-fpga-tools-ext-openroad" disks create "instance-1" --size "64" --zone "us-west2-a" --source-snapshot "snapshot-2" --type "pd-ssd"
    #gcloud beta compute disks create disk-1 --project=foss-fpga-tools-ext-openroad --type=pd-standard --size=64GB --zone=us-west2-a --source-snapshot=snapshot-3 --physical-block-size=4096    

    # make an instance from a disk
    #gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create instance-1 --zone=us-west2-a --machine-type=c2-standard-8 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=instance-1,device-name=instance-1,mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any

    #gcloud beta compute --project=foss-fpga-tools-ext-openroad instances create instance-1 --zone=us-west2-a --machine-type=c2-standard-8 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=281156998478-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=disk-1,device-name=disk-1,mode=rw,boot=yes --reservation-affinity=any

    # delete an instance and its disk
    #gcloud compute instances delete instance-1 --delete-disks=all --quiet



  687  gcloud compute ssh instance-1 -- "ls"
  688  gcloud compute ssh instance-1 -- "ls -al"
  689  gcloud compute ssh instance-1 -- "ls -al .ssh"
  690  gcloud compute ssh instance-1 -- "cat -al .ssh/authorized_keys"
  691  gcloud compute ssh instance-1 -- "cat .ssh/authorized_keys"
  692  gcloud compute ssh instance-1 -- "tocuh tom.test"
  693  gcloud compute ssh instance-1 -- "touch tom.test"
  694  gcloud compute ssh instance-1 -- "ls -al"
  695  gcloud compute ssh instance-1 -- "df ."
