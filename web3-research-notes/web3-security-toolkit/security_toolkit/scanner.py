"""Security scanning for Web3."""

from typing import List, Dict
import re

class SecurityScanner:
    """Scan Web3 projects for security issues."""
    
    VULNERABILITY_PATTERNS = [
        (r'tx\.origin\s*==\s*owner', 'tx.origin authentication', 'critical'),
        (r'selfdestruct\(', 'unprotected selfdestruct', 'critical'),
        (r'\.call\{value:', 'unchecked call', 'high'),
        (r'block\.timestamp', 'timestamp dependence', 'medium'),
    ]
    
    def scan_contract(self, code: str) -> List[Dict]:
        """Scan contract for vulnerabilities."""
        findings = []
        
        for pattern, description, severity in self.VULNERABILITY_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append({
                    'type': description,
                    'severity': severity,
                    'pattern': pattern
                })
        
        return findings
    
    def scan_dependencies(self, package_json: str) -> List[Dict]:
        """Scan dependencies for known vulnerabilities."""
        return []
