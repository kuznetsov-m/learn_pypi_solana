import json

import solana
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
import solana.system_program as sp
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import AccountMeta, Transaction, TransactionInstruction
from solana.rpc.types import TxOpts
from spl.token._layouts import ACCOUNT_LAYOUT
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


######################
# Program state account creation

test_program_keypair = [42,126,209,101,182,11,110,103,64,11,125,3,77,237,86,140,99,131,0,181,152,37,25,20,74,220,91,92,170,24,220,176,31,42,156,100,224,241,175,248,175,59,57,167,219,153,17,228,40,106,38,177,134,107,203,228,147,122,71,65,0,219,199,143]
test_program_account = Account(test_program_keypair[:32])

program_sub_account = Account()
print(f'program_sub_account pubkey: {program_sub_account.public_key()}')
# Allocate memory for the account
balance_needed = client.get_minimum_balance_for_rent_exemption(ACCOUNT_LAYOUT.sizeof()).get('result')
# Construct transaction
txn = Transaction()
txn.add(
    sp.create_account(
        sp.CreateAccountParams(
            from_pubkey=initializer_account.public_key(),
            new_account_pubkey=program_sub_account.public_key(),
            lamports=balance_needed,
            space=ACCOUNT_LAYOUT.sizeof(),
            program_id=test_program_account.public_key(),
        )
    )
)

rpc_response = client.send_transaction(
    txn,
    initializer_account, program_sub_account,
    opts=TxOpts(skip_preflight=True, skip_confirmation=False)
)
print(f'rpc_response: {rpc_response}')