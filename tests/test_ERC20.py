import pytest

def test_beforeUpgrade(web3, accounts, PROXIED_ERC20):
  failed = True
  try:
    print("Trying to get the wonderful message..")
    msg = PROXIED_ERC20.functions.getWonderfulMessage().call()
    failed = False
  except:
    pass
  assert failed, "Shouldn't get the wonderful message"
  print("Can't get the message before upgrading")

def test_afterUpgrade(web3, accounts, ERC20_UPGRADED, PROXIED_ERC20):
  failed = True
  try:
    print("Trying to get the wonderful message..")
    msg = PROXIED_ERC20.functions.getWonderfulMessage().call()
    failed = False
  except:
    pass
  assert not failed, "Should get the wonderful message"
  print(f"Got the message! {msg}")