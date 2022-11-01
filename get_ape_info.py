from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

import re

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/Users/tannernordell/Documents/UPenn MCIT Graduate Program/CIT 582 - Fall 2022/nft_attributes/abi.json', 'r') as f:
	abi = json.load(f) 
#/home/codio/workspace/abi.json

############################
#Connect to an Ethereum node
api_url = "https://eth-mainnet.g.alchemy.com/v2/NIE1PKM0OrUhraZkRFQGLC6RtQj2XIpg"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"


	
	#YOUR CODE HERE
	bayc_inst = web3.eth.contract(address=bayc_address, abi=abi)
	#total_supply = bayc_inst.functions.totalSupply().call()
	owner = bayc_inst.functions.ownerOf(apeID).call()
	ape_URI = bayc_inst.functions.tokenURI(apeID).call()

	token = re.match('ipfs://(.*)', ape_URI).group(1)
	url = f'https://gateway.pinata.cloud/ipfs/{token}'
	res = requests.get(url)
	res_json = res.json()

	image = res_json['image']
	eyes = [x['value'] for x in res_json['attributes'] if x['trait_type'] == 'Eyes'][0]

	data = {'owner': owner, 'image': image, 'eyes': eyes}

	#tokenURI

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

