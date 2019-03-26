#!/usr/bin/env python3

from web3 import Web3, HTTPProvider
import json
import argparse
from account import Account
import sys
from os.path import getmtime, join, exists, abspath


def parse_args(args):
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--network", default="http://localhost:8545", help="Enter network, defaults to testrpc")
  return parser.parse_known_args(args)

def tx_args(gas=200000, gasPrice=None, value=0, nonce=None):
  args = {"value": Web3.toWei(value, "ether"), "gas": gas, "gasPrice": gasPrice or 2000000000}
  if nonce is not None:
  	args["nonce"] = nonce
  return args

args, unknown = parse_args(sys.argv[1: ])

web3 = Web3(HTTPProvider(args.network))
gas_price = 3000000000
build_path = "build"

with open("keystore/keyfile") as key_file:
  file_content = json.load(key_file)
  deployer_address = web3.toChecksumAddress(file_content["address"])
  deployer_encrypted_key = file_content
  deployer_decryption_key = "coinfabrik123"
  deployer_decrypted_key = web3.eth.account.decrypt(deployer_encrypted_key, deployer_decryption_key)

deployer = Account(web3, build_path, deployer_address, deployer_decrypted_key)

ERC20_code_hash, ERC20_code = deployer.deploy("ERC20", tx_args(gas = 3000000, gasPrice = gas_price))
assert web3.eth.waitForTransactionReceipt(ERC20_code_hash).status == 1, "Error deploying ERC20 code."

proxy_hash, proxy = deployer.deploy("Proxy", tx_args(gas = 3000000, gasPrice = gas_price), ERC20_code.address, "0x")
assert web3.eth.waitForTransactionReceipt(proxy_hash).status == 1, "Error deploying ERC20 code."

with open("addresses.json", "w") as dump_file:
  data = {
    "proxy":proxy.address,
    "ERC20": ERC20_code.address,
    }
  json.dump(data, dump_file, indent=4)
