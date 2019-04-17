#!/bin/bash

./compile.sh;

virtualenv -p python3 ./py-venv
source ./py-venv/bin/activate
# Setup a stable development environment
pip install --upgrade pip setuptools
pip install web3 pytest

python3 fund.py

cd deploy/
./deploy.py