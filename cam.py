#!/usr/bin/env python
import os
"""Very specialized little script that searches my home network for my IP Camera, then builds an SSH tunnel to it.
Access the camera at http://localhost:8558
"""
#Make sure /usr/bin/arp-scan is added to your sudoers file


USER = "user"
HOST = "yourHost.com"
SSH = USER + "@" + HOST
MAC = "00:00:00:00:00:00"

ssh_command = "ssh " + SSH

arp_scan = "sudo arp-scan -l | grep " + MAC + " | head -n1 | awk '{print $1;}'"

stream = os.popen(ssh_command + ' ' + arp_scan)

command = "ssh -L 8558:" + stream.read() +":8558 " + SSH
stream.close()
command = command.replace('\n', '') #Strip newline from the end of the IP returned from the stream

os.system(command)
