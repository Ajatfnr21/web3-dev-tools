#!/usr/bin/env python3
"""Web3 Dev Tools CLI"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from web3_dev_tools.tools import (
    ContractDeployer, GasOptimizer, ABIGenerator, 
    ContractVerifier, EventDecoder
)

def demo_deployer():
    """Demo contract deployment prep"""
    print("=" * 70)
    print("Contract Deployment Helper Demo")
    print("=" * 70)
    
    deployer = ContractDeployer()
    
    # Sample bytecode (simplified)
    bytecode = "608060405234801561001057600080fd5b50..."
    
    gas_estimate = deployer.estimate_deployment_gas(bytecode)
    tx_data = deployer.prepare_deployment_data(bytecode)
    
    print(f"\nEstimated Gas: {gas_estimate:,}")
    print(f"At 20 Gwei: {gas_estimate * 20 / 1e9:.4f} ETH")
    print(f"At 50 Gwei: {gas_estimate * 50 / 1e9:.4f} ETH")
    print(f"\nDeployment Transaction Data:")
    print(json.dumps(tx_data, indent=2))

def demo_gas_optimizer():
    """Demo gas optimization"""
    print("\n" + "=" * 70)
    print("Gas Optimization Analyzer Demo")
    print("=" * 70)
    
    optimizer = GasOptimizer()
    
    # Sample bytecode
    bytecode = "608060405234801561001057600080fd5b50" * 10
    
    analysis = optimizer.analyze_bytecode(bytecode)
    
    print(f"\nBytecode Analysis:")
    print(f"  Total Opcodes: {analysis['total_opcodes']:,}")
    print(f"  Storage Writes (SSTORE): {analysis['storage_writes']}")
    print(f"  Estimated Gas: {analysis['estimated_gas']:,}")
    
    if analysis['issues']:
        print(f"\nOptimization Opportunities:")
        for issue in analysis['issues']:
            print(f"  ⚠️  {issue['message']}")
            print(f"     Potential Savings: {issue['potential_savings']:,} gas")
    
    # Solidity optimization suggestions
    sample_code = """
    function processItems() public {
        for (uint i = 0; i < items.length; i++) {
            storageVar[i] = items[i];  // Bad: storage in loop
        }
        
        contract1.call(data1);  // Multiple calls
        contract2.call(data2);
        contract3.call(data3);
    }
    """
    
    suggestions = optimizer.suggest_optimizations(sample_code)
    print(f"\nCode Optimization Suggestions:")
    for s in suggestions:
        print(f"  💡 {s['issue']}")
        print(f"     Fix: {s['fix']}")
        print(f"     Savings: {s['savings']}")

def demo_abi_generator():
    """Demo ABI generator"""
    print("\n" + "=" * 70)
    print("ABI Generator Demo")
    print("=" * 70)
    
    gen = ABIGenerator()
    
    sample_abi = [
        {
            "type": "function",
            "name": "transfer",
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "amount", "type": "uint256"}
            ],
            "outputs": [{"name": "", "type": "bool"}],
            "stateMutability": "nonpayable"
        },
        {
            "type": "event",
            "name": "Transfer",
            "inputs": [
                {"name": "from", "type": "address", "indexed": True},
                {"name": "to", "type": "address", "indexed": True},
                {"name": "value", "type": "uint256"}
            ]
        }
    ]
    
    parsed = gen.parse_abi(sample_abi)
    
    print(f"\nParsed ABI:")
    print(f"  Functions: {parsed['function_count']}")
    for func in parsed['functions']:
        print(f"    - {func['name']}() [{func['stateMutability']}]")
    
    print(f"\n  Events: {parsed['event_count']}")
    for event in parsed['events']:
        print(f"    - {event['name']}")

def main():
    parser = argparse.ArgumentParser(description="Web3 Dev Tools")
    subparsers = parser.add_subparsers(dest="command")
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy-prep", help="Prepare deployment")
    deploy_parser.add_argument("bytecode", help="Contract bytecode")
    
    # Gas command
    gas_parser = subparsers.add_parser("gas", help="Analyze gas usage")
    gas_parser.add_argument("--bytecode", help="Bytecode to analyze")
    gas_parser.add_argument("--code", help="Solidity code to analyze")
    
    # ABI command
    subparsers.add_parser("abi", help="ABI utilities")
    
    args = parser.parse_args()
    
    if args.command == "deploy-prep":
        print(f"Preparing deployment for {args.bytecode[:20]}...")
    elif args.command == "gas":
        print("Analyzing gas usage...")
    else:
        # Run all demos
        demo_deployer()
        demo_gas_optimizer()
        demo_abi_generator()
        
        print("\n" + "=" * 70)
        print("Web3 Dev Tools Demo Complete!")
        print("=" * 70)

if __name__ == "__main__":
    main()
