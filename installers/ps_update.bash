### VARS

FILE=https://raw.githubusercontent.com/Rkieltyka/rados/dotfiles/dotfiles/git_prompt-string.txt

USER_POSITION=8
ROOT_POSITION=11


### INSTALLER

if [ $(id -u) -ne 0 ];
    then
        echo "[ERROR] Please execute this file as root"
        echo "------> sudo ./this_file.bash"
    exit
fi

echo "Installing custom user prompt string..."
curl -s $FILE | head -n $USER_POSITION | tail -n 1 >> ~/.bashrc

echo "Installing custom ROOT prompt string..."
curl -s $FILE | head -n $ROOT_POSITION | tail -n 1 >> /root/.bashrc
