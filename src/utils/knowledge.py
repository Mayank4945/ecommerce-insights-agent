"""
External knowledge integration utilities
"""

import requests
from typing import Optional, Dict, Any, List
from src.config import config
from src.logger import get_logger

logger = get_logger(__name__)


class WebSearchProvider:
    """Web search using Tavily API"""
    
    def __init__(self):
        self.api_key = config.api.tavily_api_key
        self.enabled = config.api.enable_web_search and self.api_key
    
    def search(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search the web for information
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        if not self.enabled:
            logger.warning("Web search not enabled or API key not configured")
            return []
        
        try:
            # Tavily API integration would go here
            # For now, return empty list as it requires API key
            logger.info(f"Web search query: {query}")
            return []
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []


class WikipediaProvider:
    """Wikipedia information lookup"""
    
    @staticmethod
    def search(query: str) -> Optional[str]:
        """
        Search Wikipedia for information
        
        Args:
            query: Search query
            
        Returns:
            Summary text or None
        """
        try:
            import wikipedia
            wikipedia.set_lang('en')
            
            # Search for the query
            search_results = wikipedia.search(query, results=1)
            
            if not search_results:
                return None
            
            # Get summary
            summary = wikipedia.summary(search_results[0], sentences=3)
            return summary
            
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return None


class ProductEnrichment:
    """Enrich product information with external data"""
    
    @staticmethod
    def get_product_info(product_name: str) -> Dict[str, Any]:
        """
        Get enriched product information
        
        Args:
            product_name: Product name
            
        Returns:
            Dictionary with enriched information
        """
        try:
            # Try Wikipedia first
            wiki_info = WikipediaProvider.search(product_name)
            
            info = {
                'product_name': product_name,
                'description': wiki_info if wiki_info else 'No additional information available',
                'source': 'Wikipedia' if wiki_info else 'None'
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Product enrichment error: {e}")
            return {
                'product_name': product_name,
                'description': 'Error retrieving information',
                'source': 'Error'
            }


class KnowledgeBase:
    """Centralized knowledge base for external information"""
    
    def __init__(self):
        self.web_search = WebSearchProvider()
        self.wikipedia = WikipediaProvider()
        self.product_enrichment = ProductEnrichment()
    
    def lookup(self, query: str, source: str = 'auto') -> Optional[str]:
        """
        Lookup information from external sources
        
        Args:
            query: Search query
            source: 'web', 'wikipedia', or 'auto'
            
        Returns:
            Information string or None
        """
        try:
            if source == 'wikipedia' or source == 'auto':
                wiki_result = self.wikipedia.search(query)
                if wiki_result:
                    return f"**Wikipedia:** {wiki_result}"
            
            if source == 'web' and self.web_search.enabled:
                web_results = self.web_search.search(query)
                if web_results:
                    return self._format_web_results(web_results)
            
            return None
            
        except Exception as e:
            logger.error(f"Knowledge lookup error: {e}")
            return None
    
    def _format_web_results(self, results: List[Dict[str, Any]]) -> str:
        """Format web search results"""
        formatted = ["**Web Search Results:**\n"]
        for i, result in enumerate(results, 1):
            formatted.append(f"{i}. {result.get('title', 'No title')}")
            formatted.append(f"   {result.get('snippet', 'No description')}")
            formatted.append(f"   Source: {result.get('url', 'No URL')}\n")
        return "\n".join(formatted)
