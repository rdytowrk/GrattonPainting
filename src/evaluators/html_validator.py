"""HTML validation and structure checking."""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import html5lib


class HTMLValidator:
    """Validates HTML structure and syntax."""
    
    def __init__(self):
        """Initialize validator."""
        pass
    
    def validate(self, html: str) -> Dict[str, Any]:
        """
        Validate HTML structure.
        
        Returns:
            Dict with score (0.0-1.0), passed (bool), and details
        """
        if not html or not html.strip():
            return {
                "score": 0.0,
                "passed": False,
                "details": {
                    "error": "Empty HTML",
                    "is_valid": False
                }
            }
        
        errors = []
        warnings = []
        
        try:
            # Parse with html5lib (strict HTML5 parser)
            doc = html5lib.parse(html, treebuilder="lxml", namespaceHTMLElements=False)
            is_valid = True
        except Exception as e:
            is_valid = False
            errors.append(f"HTML5 parsing error: {str(e)}")
        
        # Also check with BeautifulSoup for additional issues
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check for basic structure issues
            if not soup.find():
                errors.append("No HTML elements found")
            
            # Check for unclosed tags (BeautifulSoup will auto-close, so this is best-effort)
            # Count opening and closing tags
            tag_counts = {}
            for tag in soup.find_all():
                tag_name = tag.name
                if tag_name not in tag_counts:
                    tag_counts[tag_name] = {"open": 0, "close": 0}
                tag_counts[tag_name]["open"] += 1
            
            # Check for inline styles (should not be present in Tailwind conversion)
            elements_with_inline_style = soup.find_all(style=True)
            if elements_with_inline_style:
                warnings.append(f"Found {len(elements_with_inline_style)} elements with inline styles")
            
        except Exception as e:
            warnings.append(f"Additional validation warning: {str(e)}")
        
        # Calculate score
        score = 1.0 if is_valid else 0.0
        
        # Reduce score for warnings (but don't fail completely)
        if warnings:
            score = max(0.5, score - (len(warnings) * 0.1))
        
        return {
            "score": score,
            "passed": is_valid and len(errors) == 0,
            "details": {
                "is_valid": is_valid,
                "errors": errors,
                "warnings": warnings,
                "elements_with_inline_styles": len(elements_with_inline_style) if 'elements_with_inline_style' in locals() else 0
            }
        }
