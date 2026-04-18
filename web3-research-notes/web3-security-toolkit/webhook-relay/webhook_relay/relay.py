"""Core webhook relay functionality."""

import asyncio
import aiohttp
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass

@dataclass
class WebhookDestination:
    url: str
    headers: Optional[Dict] = None
    filters: Optional[List[Callable]] = None
    transform: Optional[Callable] = None

class WebhookRelay:
    """Relay webhooks to multiple destinations."""
    
    def __init__(self):
        self.destinations: List[WebhookDestination] = []
        self.history = []
    
    def add_destination(self, destination: WebhookDestination):
        """Add a destination endpoint."""
        self.destinations.append(destination)
    
    async def relay(self, payload: Dict, source: str = "unknown"):
        """Relay payload to all destinations."""
        results = []
        
        for dest in self.destinations:
            try:
                # Apply filters
                if dest.filters:
                    if not all(f(payload) for f in dest.filters):
                        continue
                
                # Transform payload
                transformed = dest.transform(payload) if dest.transform else payload
                
                # Send to destination
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        dest.url,
                        json=transformed,
                        headers=dest.headers or {}
                    ) as resp:
                        results.append({
                            'destination': dest.url,
                            'status': resp.status
                        })
            except Exception as e:
                results.append({
                    'destination': dest.url,
                    'error': str(e)
                })
        
        self.history.append({
            'source': source,
            'timestamp': asyncio.get_event_loop().time(),
            'results': results
        })
        
        return results
