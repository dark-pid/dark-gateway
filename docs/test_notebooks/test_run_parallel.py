import os
import sys
import configparser

#add dark to path
src_code_dir = os.sep.join(os.path.abspath('').split(os.sep)[:-2])+os.sep
sys.path.insert(0,src_code_dir)

from dark.gateway import DarkGateway
from dark import DarkMap
from dark import DarkPid
from dark.decoder import DarkDecoder
import time


###
PROJECT_ROOT = '/home/thiago/dark/dark'
config_file = os.path.join(PROJECT_ROOT,'config.ini')
#blockchain config
bc_config = configparser.ConfigParser()
bc_config.read(config_file)
#deployed contracts config
deployed_contracts_config = configparser.ConfigParser()
deployed_contracts_config.read(os.path.join(PROJECT_ROOT,'deployed_contracts.ini'))


# Load Blockchain Drivers to the dARK GateWay
dgw =  DarkGateway(bc_config,deployed_contracts_config)
# create a map to interact with the Blockchain Smart Contracts
dm = DarkMap(dgw)


import time

sa = dgw.authority_addr

# for _ in range(15):
#     nonce = dgw.get_next_nonce(sa)
#     if nonce is not None:
#         print(f'Nonce atual: {nonce}')
#     else:
#         print('Limite de chamadas no mesmo bloco atingido.')
#     time.sleep(0.1)

# curl -X POST --data '{"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":["SEU_HASH_DA_TRANSACAO"],"id":1}' http://200.130.0.40:8545


# p = dm.sync_request_pid_hash()
pid = dm.sync_request_pid()
p = dm.get_pid_by_ark(pid).to_dict()['pid_hash']


print(3*'---')
print(pid,p)

print(3*'---')
a = dm.async_set_url(p,'uol.com')
# print('\t a',a)
a = dm.async_set_url(p,'uol.com1')
# print('\t a',a)
a = dm.async_set_url(p,'uol.com2')
# print('\t a',a)
a = dm.async_set_url(p,'uol.com3')
# print('\t a',a)

time.sleep(2)
print( '> esperando a persistencia' + 3*'---')
# print(dm.get_pid_by_ark(pid).to_dict())

print('> setando multiplos dois' + 3*'---')

t1 = time.time()
tx = []
tx.append(dm.async_set_external_pid(p,pid + '1'))
tx.append(dm.async_set_external_pid(p,pid + '12'))
tx.append(dm.async_set_external_pid(p,pid + '123'))
tx.append(dm.async_set_external_pid(p,pid + '1234'))
tx.append(dm.async_set_external_pid(p,pid + '12345'))
tx.append(dm.async_set_external_pid(p,pid + '123456'))
tx.append(dm.async_set_external_pid(p,pid + '1234567'))
tx.append(dm.async_set_external_pid(p,pid + '123456789'))
tx.append(dm.async_set_external_pid(p,pid + '1234567890'))
tx.append(dm.async_set_external_pid(p,pid + '12345678901'))
tx.append(dm.async_set_external_pid(p,pid + '123456789012'))
tx.append(dm.async_set_external_pid(p,pid + '1234567890123'))
tx.append(dm.async_set_external_pid(p,pid + '12345678901234'))
tx.append(dm.async_set_external_pid(p,pid + '123456789012345'))
t2 = time.time()
delta = t2-t1

txs = delta / len(tx)
print(f"\t {len(tx)} txs enviadas em {delta} segundos ({txs})")


time.sleep(2)
print('> esperando a persistencia' + 3*'---')
print(dm.get_pid_by_ark(pid).to_dict())
