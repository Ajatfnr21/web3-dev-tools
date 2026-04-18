"""
Web3 Dev Tools - Essential development utilities
"""
import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

@dataclass
class GasEstimate:
    function_name: str
    gas_used: int
    gas_price_gwei: float
    cost_eth: float
    cost_usd: float

class ContractDeployer:
    """Smart contract deployment helper"""
    
    def __init__(self, rpc_url: str = "https://eth.llamarpc.com"):
        self.rpc_url = rpc_url
    
    def prepare_deployment_data(self, bytecode: str, constructor_args: List = None) -> Dict:
        """Prepare transaction data for deployment"""
        data = bytecode
        
        if constructor_args:
            # Encode constructor arguments
            encoded_args = self._encode_args(constructor_args)
            data += encoded_args
        
        return {
            "from": "YOUR_ADDRESS",
            "data": data,
            "gas": "0x" + hex(self.estimate_deployment_gas(bytecode))[2:],
        }
    
    def estimate_deployment_gas(self, bytecode: str) -> int:
        """Estimate gas needed for deployment"""
        # Base cost + per-byte cost
        base_cost = 21000
        byte_cost = 200 * (len(bytecode) // 2)  # Approximate
        return base_cost + byte_cost + 50000  # Buffer
    
    def _encode_args(self, args: List) -> str:
        """Simple argument encoder (simplified)"""
        # Real implementation would use ABI encoding
        return ""

class GasOptimizer:
    """Analyze and optimize gas usage"""
    
    def __init__(self):
        self.gas_costs = {
            "SSTORE": 20000,  # Cold storage write
            "SLOAD": 2100,    # Cold storage read
            "CALL": 700,
            "STATICCALL": 700,
            "DELEGATECALL": 700,
            "CREATE": 32000,
        }
    
    def analyze_bytecode(self, bytecode: str) -> Dict:
        """Analyze bytecode for gas optimization opportunities"""
        issues = []
        
        # Check for SSTORE patterns
        sstore_count = bytecode.count("55")  # SSTORE opcode
        if sstore_count > 5:
            issues.append({
                "type": "storage_writes",
                "severity": "medium",
                "message": f"Many storage writes ({sstore_count}). Consider batching.",
                "potential_savings": sstore_count * 5000
            })
        
        return {
            "total_opcodes": len(bytecode) // 2,
            "storage_writes": sstore_count,
            "issues": issues,
            "estimated_gas": self._estimate_total_gas(bytecode)
        }
    
    def _estimate_total_gas(self, bytecode: str) -> int:
        """Rough gas estimation"""
        return len(bytecode) // 2 * 10 + 21000
    
    def suggest_optimizations(self, solidity_code: str) -> List[Dict]:
        """Suggest gas optimizations for Solidity code"""
        suggestions = []
        
        # Check for memory vs storage
        if re.search(r'for.*\(.*storage', solidity_code):
            suggestions.append({
                "line": None,
                "issue": "Storage loop variable",
                "fix": "Use memory instead of storage in loops",
                "savings": "~5000 gas per iteration"
            })
        
        # Check for repeated external calls
        if len(re.findall(r'\.call', solidity_code)) > 3:
            suggestions.append({
                "line": None,
                "issue": "Multiple external calls",
                "fix": "Batch calls or use multicall",
                "savings": "~2600 gas per call"
            })
        
        return suggestions

class ABIGenerator:
    """Generate and parse contract ABIs"""
    
    def __init__(self):
        pass
    
    def generate_function_selector(self, signature: str) -> str:
        """Generate function selector from signature"""
        # Simple keccak256 of first 4 bytes
        # Real implementation would use proper hashing
        return "0x" + signature.encode().hex()[:8]
    
    def parse_abi(self, abi: List[Dict]) -> Dict:
        """Parse ABI into readable format"""
        functions = []
        events = []
        
        for item in abi:
            if item.get("type") == "function":
                functions.append({
                    "name": item.get("name"),
                    "inputs": item.get("inputs", []),
                    "outputs": item.get("outputs", []),
                    "stateMutability": item.get("stateMutability", "nonpayable"),
                    "selector": self.generate_function_selector(item.get("name", ""))
                })
            elif item.get("type") == "event":
                events.append({
                    "name": item.get("name"),
                    "inputs": item.get("inputs", [])
                })
        
        return {
            "functions": functions,
            "events": events,
            "function_count": len(functions),
            "event_count": len(events)
        }

class ContractVerifier:
    """Verify contracts on Etherscan"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def prepare_verification_data(self, contract_address: str, 
                                   source_code: str, 
                                   compiler_version: str,
                                   optimization: bool = True) -> Dict:
        """Prepare verification payload for Etherscan"""
        return {
            "apikey": self.api_key,
            "module": "contract",
            "action": "verifysourcecode",
            "contractaddress": contract_address,
            "sourceCode": source_code,
            "codeformat": "solidity-single-file",
            "contractname": "Contract",
            "compilerversion": compiler_version,
            "optimizationUsed": "1" if optimization else "0",
            "runs": "200"
        }

class EventDecoder:
    """Decode and filter contract events"""
    
    def __init__(self, abi: List[Dict] = None):
        self.abi = abi or []
        self.event_signatures = self._build_event_signatures()
    
    def _build_event_signatures(self) -> Dict[str, str]:
        """Build event signature mapping"""
        signatures = {}
        for item in self.abi:
            if item.get("type") == "event":
                name = item.get("name")
                # Real implementation would compute proper topic hash
                signatures[name] = f"0x{name.encode().hex()[:64]}"
        return signatures
    
    def decode_log(self, log: Dict) -> Optional[Dict]:
        """Decode an event log"""
        # Simplified decoder
        return {
            "address": log.get("address"),
            "topics": log.get("topics"),
            "data": log.get("data"),
            "blockNumber": log.get("blockNumber")
        }
    
    def filter_events(self, logs: List[Dict], event_name: str) -> List[Dict]:
        """Filter logs by event name"""
        # Simplified filtering
        return [log for log in logs if event_name.lower() in str(log).lower()]
