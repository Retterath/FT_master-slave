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


