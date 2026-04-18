"""Risk scoring for transactions."""

from typing import Dict

class RiskScorer:
    """Score transaction risk."""
    
    def __init__(self):
        self.weights = {
            'high_value': 20,
            'new_address': 15,
            'contract_interaction': 10,
            'mixer': 50,
            'tornado_cash': 100
        }
    
    def score(self, analysis: Dict) -> Dict:
        """Calculate risk score."""
        score = 0
        factors = []
        
        for factor in analysis.get('risk_factors', []):
            if factor in self.weights:
                score += self.weights[factor]
                factors.append(factor)
        
        return {
            'score': min(100, score),
            'level': 'high' if score > 70 else 'medium' if score > 40 else 'low',
            'factors': factors
        }
