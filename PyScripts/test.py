from guizero import *
from tkinter import filedialog
from pathlib import Path
import paramiko, time

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
def use_key(key): #paramiko cannot parse .ppk files.
    #try:
        #TODO: Uses hosts. not keys. Change
        print("Establishing ssh connection")
        client = paramiko.SSHClient()

        client.load_system_host_keys()
        key_file = paramiko.RSAKey().from_private_key_file(key) 
        '''
        The key is yet not added in the remote machine. Use add_keys_linux() to continue
        '''
        client.connect(hostname=target_ip, port=target_port, username=target_user, 
                        allow_agent=False,look_for_keys=False, pkey=key_file)
        
        client.load_host_keys(filename=key)
        client.save_host_keys('./Keys/ft_known_hosts')
        #private_key = paramiko.RSAKey.from_private_key_file(filename=pkey)
        
        command = client.exec_command("hostname")
        print(command.read().decode())
        print("Connected to server")
    #except paramiko.AuthenticationException: print("Authentication failed, check password.")
        
use_key("C:/Users/rette/.ssh/id_rsa") #private key

def use_keys(): #Add way for paramiko to create the file itself HERE inside the project
    session = paramiko.SSHClient()
    curr_path = Path.cwd()
    curr_path = curr_path.parent
    #session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.load_host_keys('./Keys/known_hosts')
    #session.set_missing_host_key_policy(paramiko.RejectPolicy())
    #session.set_missing_host_key_policy(paramiko.WarningPolicy())
    session.connect(hostname=target_ip, username=target_user, password="161198")
    commands = ['ls /', 'echo $USER', 'hostname', 'sdfgh']
    for command in commands:
        print(f"{'#'*10} Executing the command: {command} {'#'*10}")
        stdin, stdout, stderr = session.exec_command(command)
        
        time.sleep(.5)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    session.close()

#RSA: static generate()
def add_keys_windows(): # %USERPROFILE%\.ssh\id_rsa.pub | ssh tom@192.168.1.119 "cat >> .ssh/authorized_keys"
    return 1
def add_keys_linux(): #ssh-copy-id -i ~/.ssh/id_rsa.pub tom@192.168.1.119 -p 22
    #TODO: extend functionality to send the key to remote machine
    session = paramiko.SSHClient()
    session.load_system_host_keys()
    key_file = paramiko.RSAKey.from_private_key_file("C:/Users/rette/.ssh/id_rsa")
    session.connect(hostname=target_ip, username=target_user, pkey=key_file,
                        allow_agent=False, look_for_keys=False)

    session.close()

