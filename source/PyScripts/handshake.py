import os, paramiko, subprocess
from pathlib import Path
from io import StringIO

target_ip = '192.168.1.119'
target_user = 'tom'
target_port = 22

def ping_alex(hostname):
    response = os.system('ping -c 1 ' + hostname) #UPDATE
    #and then check the response...
    if response == 0:
      print(hostname, 'is up!')
    else:
      print(hostname, 'is down!')

def ping_ssh():
    # ping to host...
    ssh_client = ssh_conn(target_ip, target_port, target_user)
    
    if ssh_client is None:
        print('Connection dead!')
    else:
        print('Connection alive!')

############
# Connect #
############
def ssh_conn(target_ip, target_pass, port):
    host_keys_path = Path('Keys','known_hosts')
    session = paramiko.SSHClient()
    try:
        host_keys = paramiko.HostKeys(host_keys_path)
    except: 
        print("Corrupted host_keys file.")
        return 0 #Add method for fixing corrupted host keys
        
    pkey = __generate_RSA_KEY(target_ip, 'd')
    session.load_host_keys(host_keys_path)
    if host_keys.lookup(target_ip) is None:
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    else:
        session.set_missing_host_key_policy(paramiko.RejectPolicy())
    
    session.connect(target_ip, username=target_user, pkey=pkey)
    session.save_host_keys(host_keys_path) 
    session.close()
def ssh_raw_conn(target_ip, target_pass):
    session = paramiko.SSHClient()
    session.load_system_host_keys()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(hostname=target_ip, password=target_pass)
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
__generate_RSA_KEY(target_ip, None)