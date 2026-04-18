"""Transaction analysis engine."""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    hash: str
    from_addr: str
    to_addr: str
    value: float
    gas_price: int
    gas_used: int
    timestamp: datetime
    data: str

class TransactionAnalyzer:
    """Analyze blockchain transactions."""
    
    def __init__(self):
        self.known_entities = {}
        self.suspicious_patterns = []
    
    def analyze(self, tx: Transaction) -> Dict:
        """Analyze a single transaction."""
        analysis = {
            'hash': tx.hash,
            'risk_factors': [],
            'entity_from': self.known_entities.get(tx.from_addr),
            'entity_to': self.known_entities.get(tx.to_addr),
            'value_usd': self._estimate_usd_value(tx.value),
        }
        
        # Check for suspicious patterns
        if tx.to_addr is None:
            analysis['risk_factors'].append('Contract creation')
        
        if len(tx.data) > 10000:
            analysis['risk_factors'].append('Large data payload')
        
        return analysis
    
    def _estimate_usd_value(self, value_eth: float) -> float:
        """Estimate USD value (mock)."""
        return value_eth * 3000  # Assume $3000/ETH
