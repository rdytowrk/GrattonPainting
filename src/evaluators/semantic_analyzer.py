"""Analyze semantic HTML5 element usage."""

from typing import Dict, Any, Set
from bs4 import BeautifulSoup


class SemanticAnalyzer:
    """Analyzes semantic HTML5 element usage."""
    
    # Semantic HTML5 elements
    SEMANTIC_ELEMENTS = {
        'header', 'nav', 'main', 'article', 'section', 'aside', 'footer',
        'figure', 'figcaption', 'mark', 'time', 'summary', 'details'
    }
    
    # Non-semantic elements (should be minimized)
    NON_SEMANTIC = {'div', 'span'}
    
    def __init__(self):
        """Initialize analyzer."""
        pass
    
    def analyze(self, html: str) -> Dict[str, Any]:
        """
        Analyze semantic HTML usage.
        
        Returns:
            Dict with score (0.0-1.0), passed (bool), and details
        """
        if not html or not html.strip():
            return {
                "score": 0.0,
                "passed": False,
                "details": {
                    "error": "Empty HTML"
                }
            }
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Count elements
            all_elements = soup.find_all()
            semantic_count = 0
            non_semantic_count = 0
            
            semantic_elements_found: Set[str] = set()
            
            for element in all_elements:
                tag_name = element.name
                
                if tag_name in self.SEMANTIC_ELEMENTS:
                    semantic_count += 1
                    semantic_elements_found.add(tag_name)
                elif tag_name in self.NON_SEMANTIC:
                    non_semantic_count += 1
            
            # Calculate semantic ratio
            total_structural = semantic_count + non_semantic_count
            if total_structural == 0:
                semantic_ratio = 0.0
            else:
                semantic_ratio = semantic_count / total_structural
            
            # Check for proper heading hierarchy
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            heading_levels = [int(h.name[1]) for h in headings]
            
            has_h1 = 1 in heading_levels
            proper_hierarchy = self._check_heading_hierarchy(heading_levels)
            
            # Calculate score
            score = semantic_ratio
            
            # Bonus for good heading structure
            if has_h1:
                score += 0.1
            if proper_hierarchy:
                score += 0.1
            
            # Cap at 1.0
            score = min(1.0, score)
            
            details = {
                "semantic_elements_count": semantic_count,
                "non_semantic_count": non_semantic_count,
                "semantic_ratio": semantic_ratio,
                "semantic_elements_used": list(semantic_elements_found),
                "total_elements": len(all_elements),
                "has_h1": has_h1,
                "proper_heading_hierarchy": proper_hierarchy,
                "heading_levels": heading_levels
            }
            
            return {
                "score": score,
                "passed": semantic_ratio >= 0.3,  # At least 30% semantic elements
                "details": details
            }
            
        except Exception as e:
            return {
                "score": 0.0,
                "passed": False,
                "details": {
                    "error": str(e)
                }
            }
    
    def _check_heading_hierarchy(self, levels: list) -> bool:
        """Check if heading levels follow proper hierarchy (no skipping)."""
        if not levels:
            return True
        
        # Should start with h1 or h2
        if levels[0] > 2:
            return False
        
        # Check for skipped levels
        for i in range(1, len(levels)):
            # Can't skip more than 1 level down
            if levels[i] > levels[i-1] + 1:
                return False
        
        return True
