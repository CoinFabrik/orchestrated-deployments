# Deployment

### Prerequisites

- Python 3 and virtualenv.
- Standard keyfile in JSON format(founded on the network that you will use).

### Deployment

There are a few scripts that will facilitate the process:

- Run first `./compile.sh` in the root directory of this repository.
- Setup the python environment by running `./setup_virtualenv.sh`
- Activate the environment `. py-venv/bin/activate`
- Modify the path in deploy_config.json so it matches the one with your keyfile.
- Run `./deploy.py` to deploy the contracts. You will be prompted for your decryption password.