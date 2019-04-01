def decryptKeyFromKeyfile(keyfilePath, decryptionKey):
  with open(keyfilePath) as key_file:
    file_content = json.load(key_file)
    address = web3.toChecksumAddress(file_content["address"])
    decrypted_key = web3.eth.account.decrypt(file_content, decryptionKey)
  return address, decrypted_key