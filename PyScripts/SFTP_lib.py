import os, paramiko, subprocess

target_ip = '151.237.63.205'
target_user = 'alex'
target_port = 1364

def ping_alex(hostname):
    response = os.system('ping -c 1 ' + hostname) #UPDATE
    #and then check the response...
    if response == 0:
      print(hostname, 'is up!')
    else:
      print(hostname, 'is down!')

def ping_ssh():
    # ping to host...
    ssh_client = __ssh_connect(target_ip, target_port, target_user)
    
    if ssh_client is None:
        print('Connection dead!')
    else:
        print('Connection alive!')

def __ssh_connect(host, p, usr): #Add functionality to choose key locations
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys('../Resources/tom_hosts')
        ssh_client.connect(hostname=host, port=p, username=usr)
    except:
        print('[!] __ssh_connect(): Unable to connect to SSH.')
        ssh_client = None
    return ssh_client
    if ssh_client:
        ssh_client.close
    
def transfer_file(client_path, server_path):
    ssh_client = __ssh_connect(target_ip, target_port, target_user)
    
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
    
    