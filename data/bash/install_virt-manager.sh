#! /bin/bash
# Installs virt-manager
# Author: Tom Retterath
# Date:
# Wisdom: Our aim in scripting should be to write clear and understandable code and avoid shortcuts if they do not add to this goal.

# 0=true, 1=false
# Prepare environment for the installation
red="\033[31m"
green="\033[32m"
blue="\033[34m"
reset="\033[0m"
clone_url='https://github.com/virt-manager/virt-manager'
ubuntu_desktop_image_url='http://releases.ubuntu.com/20.04/ubuntu-20.04.4-desktop-amd64.iso'
ubuntu_server_image_url='http://releases.ubuntu.com/20.04/ubuntu-20.04.4-live-server-amd64.iso'
##############################################
# Check dependencies (for APT based systems) #
##############################################
#TODO: Check virtualization support (*must support AMD-V or VT-x)
egrep -c '(vmx|svm)' /proc/cpuinfo
file="dependencies.txt"

while read dependency separator version
do
    # Check if line is blank
    if [ ! -z $dependency ]; then
        # The command dpkg-query returns false if the package is not installed.
        cur_version=$(dpkg-query --show --showformat='${Version}' $dependency 2> /dev/null )
        if [ $? -eq 1 ]; then
            echo -e "${red}$dependency is not installed with version $version${reset}"
            # Silently install the required dependency
            sudo apt-get install "$dependency" -qq > /dev/null
            continue
        elif $(dpkg --compare-versions $cur_version ge $version); then
            echo -e "${green}$dependency is installed with version $version${reset}"
        fi
    fi
done < $file

# Check if already exist
read -p "Where do you want to install virt-manager: " path
# The next lines creates the directory if it does not exist
if [ -d "$path" ]; then
    # If directory exists install inside it
    echo "Installing in $path"
    
elif [ ! -d "$path" ] && [ -n "$path" ]; then
    # If directory does not exist and the name is non-zero, create directory
    mkdir --mode 777 $path

elif [ ! -n "$path" ]; then
    # If path is empty create in current directory 
    echo "Installing in current working directory: $(pwd)"
    path=$(pwd)
fi

##########
# Config #
##########
cd $path
# Dont clone again if virt-manager was already downloaded 
if [ ! -d "virt-manager" ]; then
    git clone $clone_url &> /dev/null
fi
cd $path/virt-manager
pwd
# Determine shell flow
answer=${1-"y"}
if [ "$answer" == "y" ]; then
    # Automatic setup
    sudo groupadd libvirt
    #TODO: Change this. "Adding users to the libvirtd group effectively grants them root access."
    #       Try policykit to connect to the libvirtd daemon without asking for root password
    sudo usermod -aG libvirt $USER 
    #
    sudo mkdir -pv -m 777 /kvm/{disk,iso}
    sudo chown -R $USER /kvm
    cd /kvm/iso
    if [ -f "$ubuntu_desktop_image_url" ]; then
        sudo wget $ubuntu_desktop_image_url
    fi
    cd $path
    
    # The name of the VM; os we will install; os-variant (check with osinfo-query os --fields=name,short-id,family);
    # ram in MB; virtual disk where the VM will be saved with QEMU Copy-On-Write v2 format with 10GB size;
    # the VM will be accessed through VNC and will listen on all available network interfaces
    # disable auto-console opening
    # hvm=full virtualisation for the VM (VM perform better)
    # define path to ISO
    # set boot order (CD/DVD ROM then virtual hard drive) So, the virtual machine will be able to boot from the
    # image and install it on the hard drive.
    virt-install --name server-00 \
    --os-type linux \
    --os-variant ubuntu20.04 \
    --ram 2048 \
    --disk /kvm/disk/server-00.img,bus=virtio,size=10,format=qcow2 \
    --graphics vnc,listen=0.0.0.0 \
    --noautoconsole \
    --hvm \
    --cdrom /kvm/iso/ubuntu-20.04.4-desktop-amd64.iso \
    --boot cdrom,hd

    echo "yes"
else
    # Manualy setup
    echo "no"
# Terminate
fi
exit 0