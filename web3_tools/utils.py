"""Web3 utility functions."""

from web3 import Web3

class Web3Utils:
    """Utility functions for Web3."""
    
    @staticmethod
    def to_checksum_address(address: str) -> str:
        return Web3.to_checksum_address(address)
    
    @staticmethod
    def from_wei(amount: int, unit: str = 'ether') -> float:
        return Web3.from_wei(amount, unit)
    
    @staticmethod
    def to_wei(amount: float, unit: str = 'ether') -> int:
        return Web3.to_wei(amount, unit)
    
    @staticmethod
    def keccak256(text: str) -> str:
        return Web3.keccak(text=text).hex()
