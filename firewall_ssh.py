gcloud compute firewall-rules create default-allow-ssh --allow tcp:22
gcloud beta compute ssh --zone "us-west2-a" "openroad-public-jenkins-agent" --project "foss-fpga-tools-ext-openroad" -- "uname -a"

tom@openroad-PowerEdge-R300:~$ gcloud beta compute ssh --zone "us-west2-a" "openroad@openroad-public-jenkins-agent" --project "foss-fpga-tools-ext-openroad" -- "whoami"


