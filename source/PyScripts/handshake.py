import os, paramiko, subprocess
from pathlib import Path
from io import StringIO

from paramiko.client import AutoAddPolicy, SSHClient

target_ip = '192.168.122.174'
target_user = 'retterath-ubuntu-server'
target_port = 22

def ping_ssh(hostname):
    response = os.system('ping -c 1 ' + hostname) #UPDATE
    if response == 0:
      return "ON"
    return "OFF"

############
# Connect #
############
def ssh_conn(target_ip, target_pass, port):
    host_keys_path = Path('source','Keys','known_hosts')
    session = paramiko.SSHClient()
    try:
        host_keys = paramiko.HostKeys(host_keys_path)
    except: 
       print("Corrupted host_keys file.")
       return 0
        
    pkey = __generate_RSA_KEY(target_ip, None)
    session.load_host_keys(host_keys_path)
    if host_keys.lookup(target_ip) is None:
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    else:
        session.set_missing_host_key_policy(paramiko.RejectPolicy())
    #CRASHES
    session.connect(target_ip, username=target_user, pkey=pkey)
    session.save_host_keys(host_keys_path) 
    session.close()
    
def ssh_raw_conn(target_ip, target_pass, user):
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(hostname = target_ip, 
            username = user, 
            password = target_pass)
    
    return session
    
def transfer_file(client_path, server_path):
    ssh_client = ssh_conn(target_ip, target_port, target_user)
    
    if not os.path.isfile(client_path):  
        return -1 # File not found on client
    
    ftp_client = ssh_client.open_sftp()    
    try:
        ftp_client.chdir(server_path)
    except IOError:
        print(f'Server path {server_path} invalid')
        return -1
    
    open_dir = ftp_client.getcwd()    
    ftp_client.put(client_path, open_dir + '/'+ client_path.localpath)
    ftp_client.close()
    return 0
def transfer_file_window():
    make_dir = 'mkdir ~/mount'
    connect = f'sshfs {target_user}@{target_ip}:/home/ -p {target_port} ~/mount'
    subprocess.call(make_dir, shell=True)
    subprocess.call(connect, shell=True) 

############
# Generate #
############
def __generate_known_hosts():
    #Windows uses \ while Mac and Linux use / as a separator
    if not Path('Keys','known_hosts').exists():
        try:
            Path('Keys').mkdir(parents=True, exist_ok=True)
            Path('Keys','known_hosts').touch(exist_ok=True)    
        except FileExistsError: print("known_hosts already exists.")    

def __generate_RSA_KEY(target_ip, key_path):
    ssh_dir = Path.home() / '.ssh'
    rsa_dir = Path('Keys','RSA')

    if key_path is None:
        #Check OS
        for curr_file_path in ssh_dir.iterdir():
            if curr_file_path.name == 'id_rsa': #Returns private key file
                key_path = curr_file_path
        if key_path is None:
            print("Private ssh-key not found. Please select valid key path or create a new key.")
            return 1
    pkey_path = key_path

    if not rsa_dir.exists():
        try:
            Path('Keys').mkdir(parents=True, exist_ok=True)
            rsa_dir.touch(exist_ok=True)
        except FileExistsError: print("RSA already exists.")    

    f = open(pkey_path, 'r')
    keyfile = StringIO(f.read())
    f.close()
    
    pkey = paramiko.RSAKey.from_private_key(keyfile)
    pkey.write_private_key_file(rsa_dir)
    
    return pkey 
# client = SSHClient()
# client.load_host_keys('/home/retterath/.ssh/known_hosts')
# client.load_system_host_keys()
# client.set_missing_host_key_policy(AutoAddPolicy())
# client.connect('192.168.122.174', username=target_user)
# stdin, stdout, stderr = client.exec_command('hostname')
# print(f'{stdout.read().decode()}')