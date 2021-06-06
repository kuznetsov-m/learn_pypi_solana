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

example_account_1 = Account()
example_account_2 = Account()
data = 'my data'
test_program_id = PublicKey('2DULPG9KnScTtuXLtNjKkYbCnU76HfykVCJU1rszDwet')

txn = Transaction()
txn.add(
    TransactionInstruction(
        keys=[
            AccountMeta(pubkey=example_account_1.public_key(), is_signer=True, is_writable=True),
            AccountMeta(pubkey=example_account_2.public_key(), is_signer=False, is_writable=False),
        ],
        program_id=test_program_id,
        data=data
    )
)

rpc_response = client.send_transaction(
    txn,
    initializer_account, example_account_1, example_account_2,
    opts=TxOpts(skip_preflight=True, skip_confirmation=False)
)
print(f'rpc_response: {rpc_response}')