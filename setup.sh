#!/usr/bin/env bash

pip3 install invoke
pip3 install virtualenv

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate

pip3 install -r requirements.pip
inv
