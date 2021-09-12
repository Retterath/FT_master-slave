import serial
import time
import os
import sys
import json
import datetime
import paramiko
from pathlib import Path
from io import StringIO

import random

def generate_RSA_KEY(key_path):
    ssh_dir = Path.home() / '.ssh'

    if key_path is None:
        for curr_file_path in ssh_dir.iterdir():
            if curr_file_path.name == 'id_rsa': #Returns private key file
                key_path = curr_file_path
        if key_path is None:
            print("Private ssh-key not found. Please select valid key path or create a new key.")
            return 1
    key_path_private = key_path

    #open('./Keys/RSA','a').close()
    f = open(key_path_private, 'r')
    keyfile = StringIO(f.read())
    f.close()
    
    pkey = paramiko.RSAKey.from_private_key(keyfile)
    pkey.write_private_key_file('./Keys/RSA')
    
    return pkey 

def transfer_daemon(target_ip, target_usr, port, key_path, data):
    file_name = data['Timestamp'][0:10]
    host_keys_path = Path('Keys','known_hosts')
    session = paramiko.SSHClient()
    try:
        host_keys = paramiko.HostKeys(host_keys_path)
    except: 
        print("Corrupted host_keys file.")
        return 0 #Add method for fixing corrupted host keys
        
    pkey = generate_RSA_KEY(key_path)
    session.load_host_keys(host_keys_path)
    if host_keys.lookup(target_ip) is None:
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    else:
        session.set_missing_host_key_policy(paramiko.RejectPolicy())
    
    session.connect(target_ip, username=target_usr, pkey=pkey, port=port)
    session.save_host_keys(host_keys_path) 

    json_results = json.dumps(cached_results, indent = 4)
    stdin, stdout, stderr = session.exec_command('echo "{0}" >> ~/ft_logs/{1}.json'.format(json_results, file_name))
    print(stdout.read().decode())
    print(stderr.read().decode())

    session.close()

print('#########################################################################')
print('#################### FT Arduino Sensor Interpreter ######################')
print('#########################################################################')

if len(sys.argv) != 5:
    print('[!] Unsufficient arguments!')
    print('Usage: ./arduino_interpreter.py [communication port] [baud rate] [daemon ip address] [daemon ssh port] [private key path]')
    sys.exit()

comm_port = sys.argv[1]
baud_rate = int(sys.argv[2])
daem_ip_addr = sys.argv[3]
daem_ssh_port = int(sys.argv[4])
pkey_path = sys.argv[5]

# comm_port = 'a'
# baud_rate = 1
# daem_ip_addr = '192.168.1.103'
# daem_ssh_port = 1292
# pkey_path = r'C:\Users\avv77\Desktop\stuff\maikee'

target_user = 'alv'

if (not os.path.exists(pkey_path)):
    print('[!] Private key path is invalid!')
    sys.exit()


print('[#] Trying to listen on port ' + comm_port)

ser = None
cached_results = {}
last_written_time = None

while ser is None:
    try:
        ser = serial.Serial(comm_port, baud_rate, timeout=None)
    except:
        print('[!] No connection found, retrying...')


print('[#] Opened Serial terminal on port ' + str(comm_port) + ' at ' + str(baud_rate) + ' baud rate!')
print('[#] Waiting for transfer...')

while ser.isOpen():
    slave_input = ser.readline()
    print(slave_input)
    if slave_input != b"DM_RDY\r\n":
        print('[!] Didn\'t receive correct ready message at Serial, skipping...')
        continue
    print('[#] Acknowledging transfer request at Serial...')
    ser.write(b"DM_ACK")
    print('[#] Requesting EEPROM dump...')
    slave_input = ser.readline()

    mem_block = 0

    while slave_input != b'DM_END\r\n':
        curr_input = str(slave_input)[0:len(str(slave_input)) - 2]
        curr_addr = hex(mem_block)

        print(curr_addr + ': ' + curr_input)
        cached_results[curr_addr] = curr_input

        #ser.write(b"DM_RCV")
        slave_input = ser.readline()
        mem_block += 1

    last_written_time = datetime.datetime.now()
    cached_results['Timestamp'] = str(last_written_time)

    print('[#] Establishing SSH connection to daemon...')
    transfer_daemon(daem_ip_addr, target_user, daem_ssh_port, pkey_path, cached_results)

    print('[#] Dumping completed successfully at ' +  str(last_written_time))
    print('[#] Waiting for transfer...')
