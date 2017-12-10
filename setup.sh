#!/usr/bin/env bash
echo "You will ned to install mongodb before running this script."
echo "You can use docker-compose -f local_db/docker-compose.yml up -d for docker."
echo "eg...sudo dnf install mongodb mongodb-server"
echo "eg...sudo apt install mongodb-org"
pip3.6 install invoke
pip3.6 install virtualenv

virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate

pip3.6 install -r requirements.pip
inv
