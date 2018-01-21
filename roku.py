from wakeonlan import wol
import subprocess
import sys
import requests
import xml.etree.ElementTree as ET
import time

TV='tv'
TIMEOUT=1

def make_url(suffix):
    global TV
    url = "http://%s:8060/%s" % (TV, suffix)
    sys.stderr.write(url + "\n")
    return url

def http_error_wrapper(r):
    if r.status_code != 200:
        print r.status_code, r.reason
        raise r
    
def get_xml(suffix):
    url = make_url(suffix)
    r = requests.get(url, timeout=TIMEOUT)
    http_error_wrapper(r)
    return ET.fromstring(r.content)

def status():
    ret = {}
    for child in get_xml("query/device-info"):
        value = True
        if child.text in ('true', 'false'):
            value = bool(child.text)
        elif child.text:
            value = child.text
        ret[child.tag] = value
    return ret

def post(suffix):
    url = make_url(suffix)
    r = requests.post(url, timeout=TIMEOUT)
    http_error_wrapper(r)
    
def keypress(key):
    post("keypress/" + key)
    time.sleep(1)

def off():
    while(status()["power-mode"] == "PowerOn"):
        keypress("Power")

def on():
    wol.send_magic_packet('3c:59:1e:cf:a0:f0', ip_address=TV)
    while(status()["power-mode"] != "PowerOn"):
        keypress("Power")

def exec_command(command):
    if (command == 'off'):
        off()
    elif (command == 'on'):
        on()
    elif (command == 'cartoon'):
        on()
        # curl -d '' 'http://192.168.1.134:8060/launch/tvinput.dtv?ch=1.1'
        post("launch/tvinput.dtv?ch=54.4")
    elif (command == 'chromecast'):
        on()
        keypress("InputHDMI3")
    return status()

def main():
    global TV
    command = 'on' # on, cartoon, chromecast
    if len(sys.argv) == 3:
        TV = sys.argv[2]
    if len(sys.argv) == 2:
        command = sys.argv[1]
    print(exec_command(command))

if __name__ == "__main__":
    main()