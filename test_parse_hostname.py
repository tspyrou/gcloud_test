
import array as arr

retval = ['NAME        ZONE        MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP   STATUS\n', 'instance-1  us-west2-a  n1-standard-4               10.168.0.2   34.94.27.137  RUNNING\n']

inst_data = retval[1].split()
external_ip = inst_data[4]
print external_ip



