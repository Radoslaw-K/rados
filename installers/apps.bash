#!/bin/bash

PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
cd "$PARENT_PATH"

#install_vim()
#{

#}

install_git()
{
sudo apt-get install -y git

}


install_sqlite3()
{
echo "Installing sqlite3 package"
sudo apt-get install -y sqlite3

echo "Adding custom config for sqlite3 package"
cp ../dotfiles/.sqliterc /home/$USER/.sqliterc
}


install_build_tools()
{
sudo apt-get install -y bison libtool build-essential autotools-dev automake
}


install_python_tools()
{
sudo apt-get install -y python-pip
sudo pip install flake8 coverage ipython pexpect
}


install_extras()
{
sudo apt-get install -y cmatrix redshift
}


install_general()
{
sudo apt-get -y install tree httpie terminator silversearcher-ag strace screen inotify-tools
}

##################################    MAIN   ###############################################

if [ $USER == "root" ]; then
    echo "[ERROR] Not allowed to run script as: $USER. Please log in as a different user."
    exit 0
    fi


echo "Installation started..."

sudo apt-get update

install_general
install_build_tools
install_sqlite3
install_python_tools
install_extras

# SELF DESTRUCTION
sudo rm -r ../../rados
