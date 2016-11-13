# Crawly
Simple Web Application Screenshot Script
#System Requirement
This Script build for only Linux distributions, maybe in the future will be a Windows Version.
#Install Dependencies
* sudo ./depen.sh
* python crawly.py -h 
#Usage
* Scan IP range (/24) or single hostname for specific ports and take screenshot
  python crawly.py -ip 192.168.1.0 -port 80,443 -path /robots.txt
* Scan single IP or hostname from text file for specific ports and take screenshot
  python crawly.py -port 80,443 -file /root/Desktop/host_file.txt -path /robots.txt
#Updates
* Pay attention to your execution and flags inserted,more comfortable version will release in the future 
