from guizero import *
from tkinter import filedialog
from pathlib import Path
from io import StringIO
import paramiko, time, subprocess

target_ip = '192.168.1.119'
target_user = 'tom'
target_port = 22
target_password = 161198

def interactiveSSHShell():
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=target_ip, port=target_port, username=target_user, password=161198)
        while True:
            try:
                cmd = input("$> ")
                if cmd == "exit": break
                stdin, stdout, stderr = client.exec_command(cmd)
                print(stdout.read().decode())
            except KeyboardInterrupt:
                break 
        client.close()
    except Exception as err:
        print(str(err))
#interactiveSSHShell()

def select_keys(path):
    #TODO: open folder and return the file
    return 1
def generate_known_hosts():
    #Windows uses \ while Mac and Linux use / as a separator
    if not Path('Keys','known_hosts').exists():
        try:
            Path('Keys').mkdir(parents=True, exist_ok=True)
            Path('Keys','known_hosts').touch(exist_ok=True)    
        except FileExistsError: print("known_hosts already exists.")

def use_known_hosts():
    generate_known_hosts()
    if Path('Keys','known_hosts').exists():
        print("The file is created")
        
    else: print("The file is missing")
       
def generate_RSA_KEY(target_ip, key_path):
    filename = Path('Keys','known_hosts').stem
    ssh_dir = Path.home() / '.ssh'

    if key_path is None:
        for curr_file_path in ssh_dir.iterdir():
            if curr_file_path.name == 'id_rsa': #Returns private key file
                key_path = curr_file_path
        if key_path is None:
            print("Private ssh-key not found. Please select valid key path or create a new key.")
            return 1
    key_path_private = key_path

    open('./Keys/RSA','a').close()
    f = open(key_path_private, 'r')
    keyfile = StringIO(f.read())
    f.close()
    
    pkey = paramiko.RSAKey.from_private_key(keyfile)
    pkey.write_private_key_file('./Keys/RSA')
    
    return pkey 

generate_RSA_KEY(target_ip, None)

def connect(target_ip):
    host_keys_path = Path('Keys','known_hosts')
    session = paramiko.SSHClient()
    try:
        host_keys = paramiko.HostKeys(host_keys_path)
    except: 
        print("Corrupted host_keys file.")
        return 0 #Add method for fixing corrupted host keys
        
    pkey = generate_RSA_KEY(target_ip, 'd')
    session.load_host_keys(host_keys_path)
    if host_keys.lookup(target_ip) is None:
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    else:
        session.set_missing_host_key_policy(paramiko.RejectPolicy())
    
    session.connect(target_ip, username=target_user, pkey=pkey)
    session.save_host_keys(host_keys_path) 
    
    
    stdin, stdout, stderr = session.exec_command('uptime')
    print(stdout.read().decode())
       
    session.close()
connect(target_ip)   
generate_RSA_KEY(target_ip, "C:/Users/rette/.ssh/id_rsa")

#use_key("C:/Users/rette/.ssh/id_rsa") #private key

         

#RSA: static generate()
'''
If the shell is invoked explicitly, via shell=True, it is the application’s responsibility to ensure that 
all whitespace and metacharacters are quoted appropriately to avoid shell injection vulnerabilities.
'''
def add_keys_windows(pkey_path, target_user, target_pass): 
    #authorized_keysclear ???
# type %USERPROFILE%\.ssh\id_rsa.pub | ssh tom@192.168.1.119 "cat >> .ssh/authorized_keys"
#subprocess.run('"C:/Users/rette/.ssh/id_rsa.pub | ssh tom@192.168.1.119 cat >> .ssh/authorized_keys"',shell=True)
    command = f"type {pkey_path} | ssh {target_user}@192.168.1.119 'cat >> .ssh/authorized_keys'"
    return 1
def add_keys_linux(): #ssh-copy-id -i ~/.ssh/id_rsa.pub tom@192.168.1.119 -p 22
    #TODO: extend functionality to send the key to remote machine
    session = paramiko.SSHClient()
    session.load_system_host_keys()
    key_file = paramiko.RSAKey.from_private_key_file("C:/Users/rette/.ssh/id_rsa")
    session.connect(hostname=target_ip, username=target_user, pkey=key_file,
                        allow_agent=False, look_for_keys=False)

    session.close()


