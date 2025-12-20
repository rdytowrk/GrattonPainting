"""Check code quality and cleanliness."""

from typing import Dict, Any
from bs4 import BeautifulSoup


class CodeQualityChecker:
    """Checks code quality metrics."""
    
    def __init__(self):
        """Initialize checker."""
        pass
    
    def analyze(self, html: str, max_nesting: int = 8) -> Dict[str, Any]:
        """
        Check code quality.
        
        Args:
            html: HTML to analyze
            max_nesting: Maximum acceptable nesting depth
            
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
            
            issues = []
            score = 1.0
            
            # Check 1: No inline styles
            elements_with_inline_styles = soup.find_all(style=True)
            if elements_with_inline_styles:
                issues.append(f"Found {len(elements_with_inline_styles)} elements with inline styles")
                score -= 0.3
            
            # Check 2: Check nesting depth
            max_depth = self._get_max_nesting_depth(soup)
            if max_depth > max_nesting:
                issues.append(f"Nesting depth ({max_depth}) exceeds maximum ({max_nesting})")
                score -= 0.2
            
            # Check 3: Proper indentation (check if prettified version is similar to input)
            # This is a rough heuristic
            lines = html.strip().split('\n')
            properly_indented_lines = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                
                # Check if line has some indentation (unless it's the first tag)
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces > 0 or stripped.startswith('<html') or stripped.startswith('<!DOCTYPE'):
                    properly_indented_lines += 1
            
            indentation_ratio = properly_indented_lines / len([l for l in lines if l.strip()]) if lines else 0
            
            if indentation_ratio < 0.5:
                issues.append("Poor indentation")
                score -= 0.2
            
            # Check 4: Avoid excessive div usage
            all_elements = soup.find_all()
            divs = soup.find_all('div')
            
            if all_elements:
                div_ratio = len(divs) / len(all_elements)
                if div_ratio > 0.6:  # More than 60% divs
                    issues.append(f"Excessive div usage ({div_ratio:.1%} of elements)")
                    score -= 0.2
            
            # Check 5: Reasonable element count
            element_count = len(all_elements)
            if element_count > 1000:
                issues.append(f"Very large element count ({element_count})")
                score -= 0.1
            
            # Ensure score doesn't go below 0
            score = max(0.0, score)
            
            details = {
                "max_nesting_depth": max_depth,
                "total_elements": element_count,
                "div_count": len(divs),
                "div_ratio": len(divs) / element_count if element_count > 0 else 0,
                "inline_styles_count": len(elements_with_inline_styles),
                "indentation_ratio": indentation_ratio,
                "line_count": len(lines),
                "issues": issues
            }
            
            return {
                "score": score,
                "passed": score >= 0.6,
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
    
    def _get_max_nesting_depth(self, element, current_depth=0) -> int:
        """Recursively calculate maximum nesting depth."""
        if not hasattr(element, 'children'):
            return current_depth
        
        max_child_depth = current_depth
        
        for child in element.children:
            if hasattr(child, 'name') and child.name:
                child_depth = self._get_max_nesting_depth(child, current_depth + 1)
                max_child_depth = max(max_child_depth, child_depth)
        
        return max_child_depth
