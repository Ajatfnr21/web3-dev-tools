"""Contract deployment tools."""

from web3 import Web3
from typing import Dict, Any, Optional

class ContractDeployer:
    """Deploy smart contracts to Ethereum networks."""
    
    def __init__(self, provider_url: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.w3.eth.account.from_key(private_key)
    
    def deploy(self, bytecode: str, abi: list, constructor_args: list = None) -> str:
        """Deploy contract."""
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        tx = Contract.constructor(*constructor_args).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('20', 'gwei')
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt.contractAddress
