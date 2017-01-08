#!/bin/bash

install_sqlite3()
{
echo "Installing sqlite3 package"
sudo apt-get install -y sqlite3

echo "Adding custom config for sqlite3 package"

SQLITE_RC="\
.header on
.mode column\n"

printf "$SQLITE_RC" > /home/$USER/.sqliterc

exit 0
}

##################################    MAIN   ###############################################

if [ $USER == "root" ]; then
    echo "[ERROR] Not allowed to run script as: $USER. Please log in as a different user."
    exit 0
    fi


echo "Installation started..."

sudo apt-get update

install_sqlite3

