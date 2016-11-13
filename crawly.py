#/usr/bin/python

import sys
import time
import os
import requests
import argparse
import re
import random
import Queue
from termcolor import colored
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#scan url and get screenshot with parameters
def scan_ip(iptoscan,port,path,uri):
    global number
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    dcap["phantomjs.page.settings.javascriptEnabled"] = True
    try:
        req = requests.get(uri+iptoscan+str(number)+":"+str(port)+str(path),timeout=10, verify = False)
        print colored("URL:"+uri+iptoscan+str(number)+":"+str(port)+str(path)+" status code: "+str(req.status_code), "green")
        if (req.status_code):
            br = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--webdriver-loglevel=NONE'],desired_capabilities = dcap)
            br.maximize_window()
            rand = random.randint(0,1000)
            br.get(uri+iptoscan+str(number)+":"+str(port)+str(path))
            br.save_screenshot('ss/'+str(port)+"."+str(req.status_code)+"."+iptoscan+str(number)+"."+str(rand)+".png")
            print colored("Saving ss/"+str(port)+"."+str(req.status_code)+"."+iptoscan+str(number)+"."+str(rand)+".png","red")
            br.quit
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        return None

#scan gost and get screenshot with paramters
def scan_host(iptoscan,ports,path):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    dcap["phantomjs.page.settings.javascriptEnabled"] = True
    for port in ports:
        if((port == "443") or (port == "8443")):
            uri = "https://"
        else:
            uri="http://"
        try:
            req = requests.get(uri+iptoscan+":"+str(port)+str(path),timeout=6,verify=True)
            print colored("URL: "+uri+iptoscan+":"+str(port)+str(path)+" status code: "+str(req.status_code), "green")
            if (req.status_code): 
                br = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any','--webdriver-loglevel=NONE'],desired_capabilities = dcap)
                br.maximize_window()
                rand = random.randint(0,1000)
                br.get(uri+iptoscan+":"+str(port)+str(path))
                br.save_screenshot('ss/'+str(port)+"."+str(req.status_code)+"."+iptoscan+".png")
                print colored('Saving: '+str(port)+"."+str(req.status_code)+"."+iptoscan+".png","red")
                br.quit
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            return None

def take_num():
    global number
    number+=1

#main function
def main():
    print """
  /$$$$$$                                   /$$          
 /$$__  $$                                 | $$          
| $$  \__/  /$$$$$$  /$$$$$$  /$$  /$$  /$$| $$ /$$   /$$
| $$       /$$__  $$|____  $$| $$ | $$ | $$| $$| $$  | $$
| $$      | $$  \__/ /$$$$$$$| $$ | $$ | $$| $$| $$  | $$
| $$    $$| $$      /$$__  $$| $$ | $$ | $$| $$| $$  | $$
|  $$$$$$/| $$     |  $$$$$$$|  $$$$$/$$$$/| $$|  $$$$$$$
 \______/ |__/      \_______/ \_____/\___/ |__/ \____  $$
                                                /$$  | $$
    Web Application ScreenShot Script           |  $$$$$$/
         By eran@cyberint.com                    \______/ 
    """
    #Define The ArgParse
    parser = argparse.ArgumentParser(
        description = "Crawly v1.1",
        epilog = ''' Basic Usage: 
        python crawly.py -ip 192.168.1.0 or example.com -port 80
        python crawly.py -port 80 -file /root/Desktop/host_file.txt''',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-ip', help='e.g: 192.168.1.0 wil scan the /24 hosts or example.com' , required=False)
    parser.add_argument('-port', help='e.g: 80,443,8080', required=True)
    parser.add_argument('-path', help='e.g: /index.php', required=False)
    parser.add_argument('-file', help='e.g: /root/Desktop/host_file.txt', required=False)
    args = parser.parse_args()

    global number
    global file_now
    number = 0
    threads = 5
    ports = args.port.split(",")
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    queue = Queue.Queue()

    if not (os.path.exists('ss')):
        os.makedirs('ss')

    if(args.path):
        path = args.path
    else:
        path = ""

    if (args.file):
        fname = args.file
        jobs = []
        print "Initiating scan on: "+colored(fname,'green')+" ports: "+colored(str(ports),'green')
        print ""
        try:
            hostfile = open(args.file,"r")
            for line in hostfile:
                if (line != "\r\n"):
                    queue.put(line)
            for i in range(queue.qsize()):
                for i in range(int(threads)):
                        p = multiprocessing.Process(target=scan_host, args=(queue.get().rstrip(),ports,path))
                        jobs.append(p)
                        p.start()
                        if (queue.qsize() == 0):
                            queue.task_done()
                            sys.exit(0)

        except KeyboardInterrupt:
            sys.exit(0)
        except:
            return None
    else:
        if("http://" in args.ip):
            ip = args.ip.strip('http://')
        if("https://" in args.ip):
            ip = args.ip.strip('https://')
        if (re.match(pat, args.ip)):
            ips = args.ip.split("/")
            tempip = ips[0].split(".")
            iptoscan = tempip[0]+"."+tempip[1]+"."+tempip[2]+"."
            delta = 255 / int(threads)    
            jobs = []
            
            print "Initiating scan on: "+colored(iptoscan+"0/24",'green')+" ports: "+colored(str(ports),'green')
            print ""
            for k in ports:
                if((k == "443") or (k == "8443")):
                    uri = "https://"
                else:
                    uri="http://"
                for j in range(delta):
                    for i in range(int(threads)):
                        take_num();
                        p = multiprocessing.Process(target=scan_ip, args=(iptoscan,k,path,uri))
                        jobs.append(p)
                        p.start()
                number = 0
        else:  
            iptoscan = args.ip
            print "Initiating scan on: "+colored(iptoscan,'green')+" ports: "+colored(str(ports),'green')
            print ""
            for k in ports:
                if((k == "443") or (k == "8443")):
                    uri = "https://"
                else:
                    uri="http://" 
                scan_host(iptoscan,k,path,uri)


if __name__ == '__main__':
    main()