#!/usr/bin/env bash
echo "You will ned to install mongodb before running this script."
echo "You can use docker-compose -f local_db/docker-compose.yml up -d for docker."
echo "eg...sudo dnf install mongodb mongodb-server"
echo "eg...sudo apt install mongodb-org"
pip3 install invoke
pip3 install virtualenv

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate

pip3 install -r requirements.pip
inv
