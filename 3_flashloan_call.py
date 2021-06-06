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

sourceLiquidityPubkey = 'C7PhDXuS9H6a5GfdUrEsakmVWokXRv6jfbRDiAPpVEtE'
reservePubkey = 'Bfs6BTc2t6Epb9hjGpLpQcSmQ1ZycKsEv6mV3QuV3VzZ'
lendingMarketPubkey = '9cu7LXZYJ6oNNi7X4anv2LP8NP58h8zKiE61LMcgJt5h'
lendingMarketDerivedAuthorityPubkey = '4B3rs3z48eW1iw3JNTrQZsTJnCqEbFMuGVk3TVMAtQeM'
flashLoanFeeReceiverPubkey = 'ESApvknZkcGwee2rhjL7yGKyabtdCvDJ28US8VhsWutw'
flashLoanFeeReceiverMintPubkey = 'So11111111111111111111111111111111111111112'
hostFeeReceiverPubkey = '6oLtsmgq3kMTJs11eM4rpdcQjyMAXw84VvTUAi2XHnqu'

url = 'http://127.0.0.1:8899'
url = 'https://api.devnet.solana.com'
client = Client(url)

def create_destination_liquidity() -> Account:
    account = Account()
    return account

token_lending_program_pubkey = PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
token_lending_program_pubkey = PublicKey('6h5geweHee42FbxZrYAcYJ8SGVAjG6sGow5dtzcKtrJw')


source_liquidity_publickey = PublicKey(sourceLiquidityPubkey)
reserve_publickey = PublicKey(reservePubkey)
lending_market_publickey = PublicKey(lendingMarketPubkey)
lending_market_derived_authority_publickey = PublicKey(lendingMarketDerivedAuthorityPubkey)
flash_loan_fee_receiver_publickey = PublicKey(flashLoanFeeReceiverPubkey)
flash_loan_fee_receiver_mint_publickey = PublicKey(flashLoanFeeReceiverMintPubkey)
host_fee_receiver_publickey = PublicKey(hostFeeReceiverPubkey)

destination_liquidity_account = create_destination_liquidity()


amount = 1 * 10 ** 8       # 1 0000 0000
tag = 0
data = tag.to_bytes(1, byteorder='big') + amount.to_bytes(8, byteorder='big')

txn = Transaction()
txn.add(
    TransactionInstruction(
        keys=[
            AccountMeta(pubkey=source_liquidity_publickey, is_signer=False, is_writable=True),
            AccountMeta(pubkey=destination_liquidity_account.public_key(), is_signer=False, is_writable=True),
            AccountMeta(pubkey=lending_market_publickey, is_signer=False, is_writable=False),
            AccountMeta(pubkey=lending_market_derived_authority_publickey, is_signer=False, is_writable=False),
            AccountMeta(pubkey=token_lending_program_pubkey, is_signer=False, is_writable=False),
            AccountMeta(pubkey=flash_loan_fee_receiver_publickey, is_signer=False, is_writable=True),
            AccountMeta(pubkey=host_fee_receiver_publickey, is_signer=False, is_writable=True),            
        ],
        program_id=token_lending_program_pubkey,
        data=data
    )
)

keypair = [104,199,171,119,244,99,119,192,178,248,101,99,210,7,16,254,175,172,71,30,133,195,233,4,140,160,200,15,118,185,111,248,204,23,15,233,245,121,230,144,133,86,150,182,131,223,53,254,213,165,140,242,48,142,52,42,224,101,148,220,105,116,171,180]
my_tmp_account = Account(keypair[:32])
print(f'my_tmp_account: {my_tmp_account.public_key()}')

rpc_response = client.send_transaction(
    txn,
    my_tmp_account,
    opts=TxOpts(skip_preflight=True, skip_confirmation=False)
)
print(f'rpc_response: {json.dumps(rpc_response, indent=2)}')

# output
# my_tmp_account: EjgZsApz7CFqSHPqxKS7UYXdmnEP39UviXo5D6TWLhDM
# Transaction error: {'InstructionError': [0, {'Custom': 0}]}
# rpc_response: {
#   "jsonrpc": "2.0",
#   "result": {
#     "blockTime": 1623012362,
#     "meta": {
#       "err": {
#         "InstructionError": [
#           0,
#           {
#             "Custom": 0
#           }
#         ]
#       },
#       "fee": 5000,
#       "innerInstructions": [],
#       "logMessages": [
#         "Program 6h5geweHee42FbxZrYAcYJ8SGVAjG6sGow5dtzcKtrJw invoke [1]",
#         "Program log: Pubkey cannot be unpacked",
#         "Program log: Failed to unpack instruction data",
#         "Program 6h5geweHee42FbxZrYAcYJ8SGVAjG6sGow5dtzcKtrJw consumed 2712 of 200000 compute units",
#         "Program 6h5geweHee42FbxZrYAcYJ8SGVAjG6sGow5dtzcKtrJw failed: custom program error: 0x0"
#       ],
#       "postBalances": [
#         913048280,
#         23049280,
#         0,
#         2039280,
#         2049280,
#         2463840,
#         0,
#         1141440
#       ],
#       "postTokenBalances": [],
#       "preBalances": [
#         913053280,
#         23049280,
#         0,
#         2039280,
#         2049280,
#         2463840,
#         0,
#         1141440
#       ],
#       "preTokenBalances": [],
#       "rewards": [],
#       "status": {
#         "Err": {
#           "InstructionError": [
#             0,
#             {
#               "Custom": 0
#             }
#           ]
#         }
#       }
#     },
#     "slot": 60905580,
#     "transaction": {
#       "message": {
#         "accountKeys": [
#           "EjgZsApz7CFqSHPqxKS7UYXdmnEP39UviXo5D6TWLhDM",
#           "C7PhDXuS9H6a5GfdUrEsakmVWokXRv6jfbRDiAPpVEtE",
#           "49xPAb3dy8Qa7Y6ZhFy8ZU8Q2kU9oG9x86zbtYqi9Sai",
#           "ESApvknZkcGwee2rhjL7yGKyabtdCvDJ28US8VhsWutw",
#           "6oLtsmgq3kMTJs11eM4rpdcQjyMAXw84VvTUAi2XHnqu",
#           "9cu7LXZYJ6oNNi7X4anv2LP8NP58h8zKiE61LMcgJt5h",
#           "4B3rs3z48eW1iw3JNTrQZsTJnCqEbFMuGVk3TVMAtQeM",
#           "6h5geweHee42FbxZrYAcYJ8SGVAjG6sGow5dtzcKtrJw"
#         ],
#         "header": {
#           "numReadonlySignedAccounts": 0,
#           "numReadonlyUnsignedAccounts": 3,
#           "numRequiredSignatures": 1
#         },
#         "instructions": [
#           {
#             "accounts": [
#               1,
#               2,
#               5,
#               6,
#               7,
#               3,
#               4
#             ],
#             "data": "111119qXWw",
#             "programIdIndex": 7
#           }
#         ],
#         "recentBlockhash": "9LNyPEhX7e58hhYHPXLhfnwQT8ybzgsRnfgDhSKxh1xn"
#       },
#       "signatures": [
#         "c4E8SggDHsGiyVYF22YZgKJNvoW1YKUEUNRrM5rde6sFTnxupuEqZcdxAc3KwNG4DMhEGcBftBUfGtGVLFRJW2C"
#       ]
#     }
#   },
#   "id": 5
# }