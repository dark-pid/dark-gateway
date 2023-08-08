import os
import time
import logging

import secrets

import solcx
from web3.exceptions import TransactionNotFound


from ..gateway import DarkGateway


def invoke_contract_sync(dark_gateway: DarkGateway,
                    signed_tx):
        
        assert type(dark_gateway) == DarkGateway, "dark_gateway must be a DarkGateway object"

        # signed_tx = dark_gateway.signTransaction(smart_contract,method,*args)
        tx_hash = dark_gateway.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = dark_gateway.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt, tx_hash

def invoke_contract_async(dark_gateway: DarkGateway,
                    signed_tx):
        
        assert type(dark_gateway) == DarkGateway, "dark_gateway must be a DarkGateway object"

        # signed_tx = dark_gateway.signTransaction(smart_contract,method,*args)
        tx_hash = dark_gateway.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash