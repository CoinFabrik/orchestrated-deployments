#!/usr/bin/env python3
import pytest
import os
from contract import Deployer
from tx_args import tx_args
from web3 import Web3
import json
import time

#-----------------------------------------------------------------------------------------------------------------------------
build_path = "../build"
with open("../networks.json", "r") as net_file:
  config = json.load(net_file)

@pytest.fixture(scope="module")
def web3():
  web3 = Web3(Web3.HTTPProvider(config["testNode"]))
  assert web3.isConnected(), "Cannot establish connection with ethereum node."
  return web3

@pytest.fixture(scope="module")
def accounts(web3):
  class Accounts:
    owner=web3.eth.accounts[0]
    admin=web3.eth.accounts[1]
  return Accounts

@pytest.fixture(scope="module")
def ERC20_CODE(web3, mine_tx, accounts):
  deployer = Deployer(web3, build_path)
  tx = tx_args(accounts.owner, gas=4500000)
  tx_hash, ERC20_CODE = deployer.deploy("ERC20", tx)
  mine_tx(tx_hash, what="ERC20 code deploy")
  return ERC20_CODE

@pytest.fixture(scope="module")
def WONDER_ERC20_CODE(web3, mine_tx, accounts):
  deployer = Deployer(web3, build_path)
  tx = tx_args(accounts.owner, gas=4500000)
  tx_hash, WONDER_ERC20_CODE = deployer.deploy("WonderfulERC20", tx)
  mine_tx(tx_hash, what="Wonderful ERC20 code deploy")
  return WONDER_ERC20_CODE

@pytest.fixture(scope="module")
def PROXY(web3, mine_tx, accounts, ERC20_CODE):
  deployer = Deployer(web3, build_path)
  tx = tx_args(accounts.admin, gas=4500000)
  tx_hash, proxy = deployer.deploy("Proxy", tx, ERC20_CODE.address, "0x")
  mine_tx(tx_hash, what="proxy deploy")
  return proxy

@pytest.fixture(scope="module")
def PROXIED_ERC20(web3, PROXY):
  deployer = Deployer(web3, build_path)
  proxied_erc20 = deployer.instantiate_contract("WonderfulERC20", PROXY.address)
  return proxied_erc20

@pytest.fixture(scope="module")
def ERC20_UPGRADED(mine_tx, accounts, PROXY, ERC20_CODE, WONDER_ERC20_CODE):
  deployer = Deployer(web3, build_path)
  tx = tx_args(accounts.admin, gas=4500000)
  upgrade_hash = PROXY.functions.upgradeTo(WONDER_ERC20_CODE.address).transact(tx)
  mine_tx(upgrade_hash, what="ERC20 upgrade")

@pytest.fixture(scope="module")
def mine_tx(web3):
  def mine(txhash, what):
    assert txhash is not None, "Transaction not published"
    receipt = web3.eth.waitForTransactionReceipt(txhash, 5)
    if receipt.status == 1:
      print("The {} transaction used {} gas.".format(what, receipt.gasUsed))
    return receipt
  return mine
