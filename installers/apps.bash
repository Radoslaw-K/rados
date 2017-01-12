#!/bin/bash

# Allow for relative paths
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
cd "$PARENT_PATH"


install_vim()
{
curlcheck=$(curl --version | head -n 1 | tr " " "\n" | head -n 1)
if [ $curlcheck != "curl" ]; then 
    sudo apt-get install -y curl
fi

sudo apt-get install -y vim

echo "Adding custom config for vim"
cp ../dotfiles/.vimrc /home/$USER/

echo "Updating .bashrc for vim"
printf "\n\n" >> /home/$USER/.bashrc
cat ../dotfiles/dependencies/bashrc_vimrc.update >> /home/$USER/.bashrc

echo "Downloading plugin installer for vim"
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

echo "Starting the installation of vim plugins"
vim +PlugInstall +qall
}


install_git()
{
sudo apt-get install -y git

git config --global user.name Radoslaw Kieltyka
git config --global user.email rkieltyka@dataplicity.com
git config credential.helper 'cache --timeout=9000'

git remote add wf-specialproj-pub https://github.com/wildfoundry/specialprojects-public
git remote add wf-specialproj-priv https://github.com/wildfoundry/specialprojects
git remote add wf-wfos https://github.com/wildfoundry/wf-os
git remote add rados https://github.com/Radoslaw-K/rados

vimcheck=$(vim --version | head -n 1 | tr " " "\n" | head -n 1)
if [ $vimcheck == "VIM" ]; then 
    git config --global core.editor vim
fi
}


install_sqlite3()
{
echo "Installing sqlite3 package"
sudo apt-get install -y sqlite3

echo "Adding custom config for sqlite3 package"
cp ../dotfiles/.sqliterc /home/$USER/
}


install_build_tools()
{
sudo apt-get install -y bison libtool build-essential autotools-dev automake zlib1g-dev libglib2.0-dev libpixman-1-dev flex
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


install_prompt_strings()
{

teecheck=$(tee --version | head -n 1 | tr " " "\n" | head -n 1)
if [ $teecheck != "tee" ]; then 
    sudo apt-get install -y tee
fi

gitcheck=$(git --version | head -n 1 | tr " " "\n" | head -n 1)
if [ $gitcheck == "git" ]; then
    user_ps_command="export PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w $(__git_ps1 " <%s>") \$\[\033[00m\] '"
else
    user_ps_command="export PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w \$\[\033[00m\] '"
fi


root_ps_command="export PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[1;31m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w #\[\033[00m\] '"

echo $user_ps_command >> /home/$USER/.bashrc
echo $root_ps_command | sudo tee --append /root/.bashrc > /dev/null
}


install_bashrc_extras()
{
printf "\n\n" >> /home/$USER/.bashrc
cat ../dotfiles/dependencies/bashrc_commands.extras >> /home/$USER/.bashrc
}


install_all()
{
install_general
install_extras
install_python_tools
install_build_tools
install_sqlite3
install_git
install_vim
install_prompt_strings
install_bashrc_extras
}


##################################    MAIN   ###############################################

if [ $USER == "root" ]; then
    echo "[ERROR] Not allowed to run script as: $USER. Please log in as a different user."
    exit 0
fi


# TO DO - Add --help for each installer to display the list of
# packages that will be installed and their description.

echo "
Usage: 
source apps.bash
install_<installer>

Available installers:
all
git
vim
prompt_strings
general
sqlite3
extras
python_tools
build_tools
bashrc_extras
"
