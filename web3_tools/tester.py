"""Contract testing utilities."""

from typing import Any, Dict
import json

class ContractTester:
    """Test smart contract functions."""
    
    def __init__(self, w3_instance):
        self.w3 = w3_instance
    
    def test_function(self, contract, function_name: str, args: list = None) -> Dict:
        """Test a contract function."""
        try:
            func = getattr(contract.functions, function_name)
            result = func(*args).call() if args else func().call()
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def estimate_gas(self, contract, function_name: str, args: list = None) -> int:
        """Estimate gas for function call."""
        func = getattr(contract.functions, function_name)
        return func(*args).estimateGas() if args else func().estimateGas()
