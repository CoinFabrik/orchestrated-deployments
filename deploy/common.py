from os import getenv
from web3 import Web3
import json

def getFromJsonOrEnv(file, var):
  try:
    with open(file, "r") as _file:
      file_content = json.load(_file)
      variable = file_content[var]
    assert variable is not None, f"Can't reach {var} from file."  
    print(f"Getting {var} from {file} file")
    return variable
  except FileNotFoundError as err:
    variable = getenv(var) 
    assert variable is not None, f"Can't reach {var} from environment."
    print(f"Getting {var} from environment.")
    return variable

def tx_args(gas=200000, gasPrice=3000000000, value=0, nonce=None):
  args = {"value": Web3.toWei(value, "ether"), "gas": gas, "gasPrice": gasPrice or 2000000000}
  if nonce is not None:
    args["nonce"] = nonce
  return args

def decryptKeyFromKeyfile(web3, keyfilePath, decryptionKey):
  with open(keyfilePath) as key_file:
    file_content = json.load(key_file)
    address = web3.toChecksumAddress(file_content["address"])
    decrypted_key = web3.eth.account.decrypt(file_content, decryptionKey)
  return address, decrypted_key  