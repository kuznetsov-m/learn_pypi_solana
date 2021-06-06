import json

import solana
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
import solana.system_program as sp
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import AccountMeta, Transaction, TransactionInstruction
from solana.rpc.types import TxOpts
from spl.token._layouts import ACCOUNT_LAYOUT
from spl.token.instructions import AuthorityType
from solana.account import Account
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.rpc.commitment import Recent, Root

url = 'http://127.0.0.1:8899'
client = Client(url)

keypair = [104,199,171,119,244,99,119,192,178,248,101,99,210,7,16,254,175,172,71,30,133,195,233,4,140,160,200,15,118,185,111,248,204,23,15,233,245,121,230,144,133,86,150,182,131,223,53,254,213,165,140,242,48,142,52,42,224,101,148,220,105,116,171,180]
initializer_account = Account(keypair[:32])
initializer_balance = client.get_balance(initializer_account.public_key(), commitment=Recent).get('result').get('value')

if initializer_balance == 0:
    client.request_airdrop(initializer_account.public_key(), lamports=1 * 10 ** 9, commitment=Root)
    initializer_balance = client.get_balance(initializer_account.public_key(), commitment=Recent).get('result').get('value')

print(f'initializer_account: {initializer_account.public_key()} balance: {initializer_balance}')

# #####################
# create token_x_account (owner: initializer_account)
token_x_mint_account = Account()

token_x = Token.create_mint(
    client,
    payer=initializer_account,
    mint_authority=token_x_mint_account.public_key(),
    decimals=8,
    program_id=TOKEN_PROGRAM_ID
)
print(f'token_x mint pubkey: {token_x.pubkey}')

token_x_account_pubkey = token_x.create_account(
    owner=initializer_account.public_key()
)
print(f'token_x_account_pubkey: {token_x_account_pubkey}')

# ######################
# transfer ownership of token_x_account to test_program

test_program_keypair = [42,126,209,101,182,11,110,103,64,11,125,3,77,237,86,140,99,131,0,181,152,37,25,20,74,220,91,92,170,24,220,176,31,42,156,100,224,241,175,248,175,59,57,167,219,153,17,228,40,106,38,177,134,107,203,228,147,122,71,65,0,219,199,143]
test_program_account = Account(test_program_keypair[:32])
print(f'test_program_account pubkey: {test_program_account.public_key()}')

rpc_response = token_x.set_authority_custum(
    account=token_x_account_pubkey,
    current_authority=initializer_account.public_key(),
    authority_type=AuthorityType.ACCOUNT_OWNER,
    new_authority=test_program_account.public_key()
)
print(f'rpc_response: {rpc_response}')

# output:
# initializer_account: EjgZsApz7CFqSHPqxKS7UYXdmnEP39UviXo5D6TWLhDM balance: 974776160
# token_x mint pubkey: DXg9FWw4Ue5tkq7eZehFxRb4KTco1vigz3hCq39Df7X7
# token_x_account_pubkey: 2ywBg8iLhaZxs5or96UtMAuzqMRxV3VawenQeH7oGDCs
# test_program_account pubkey: 36fKnjRiRPArHrrjpuN4eCTb9RtQHSALpychq7eAZuTk
# rpc_response: {'jsonrpc': '2.0', 'result': '3xRYf7PjyC26AFDPB1VbgyD9sfenEszvo34b3ETBYYUoH2SZubxxduwFutSpgvWXV21LN7FknvQupHptwE7FQrp6', 'id': 19}