"""Risk analysis for Web3 projects."""

from typing import Dict

class RiskAnalyzer:
    """Analyze risk in DeFi and NFT projects."""
    
    def analyze_contract(self, contract_data: Dict) -> Dict:
        """Analyze contract risk factors."""
        risk_score = 0
        factors = []
        
        if contract_data.get('has_selfdestruct'):
            risk_score += 50
            factors.append('Selfdestruct capability')
        
        if contract_data.get('is_upgradeable'):
            risk_score += 20
            factors.append('Upgradeable contract')
        
        return {
            'risk_score': min(100, risk_score),
            'risk_level': 'high' if risk_score > 60 else 'medium' if risk_score > 30 else 'low',
            'factors': factors
        }
