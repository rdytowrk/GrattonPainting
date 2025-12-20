"""Check accessibility compliance."""

from typing import Dict, Any
from bs4 import BeautifulSoup


class AccessibilityChecker:
    """Checks basic accessibility compliance."""
    
    def __init__(self):
        """Initialize checker."""
        pass
    
    def analyze(self, html: str) -> Dict[str, Any]:
        """
        Check accessibility compliance.
        
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
            checks_passed = 0
            total_checks = 0
            
            # Check 1: Images have alt text
            total_checks += 1
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            
            if not images:
                checks_passed += 1  # No images, so this check passes
            elif not images_without_alt:
                checks_passed += 1
            else:
                issues.append(f"{len(images_without_alt)} images missing alt text")
            
            # Check 2: Form inputs have labels or aria-labels
            total_checks += 1
            inputs = soup.find_all(['input', 'select', 'textarea'])
            inputs_without_labels = []
            
            for input_elem in inputs:
                input_type = input_elem.get('type', 'text')
                # Skip hidden and submit/button inputs
                if input_type in ['hidden', 'submit', 'button']:
                    continue
                
                # Check for associated label or aria-label
                has_label = False
                input_id = input_elem.get('id')
                
                if input_id:
                    # Look for label with for attribute
                    label = soup.find('label', attrs={'for': input_id})
                    if label:
                        has_label = True
                
                # Check for aria-label or aria-labelledby
                if input_elem.get('aria-label') or input_elem.get('aria-labelledby'):
                    has_label = True
                
                # Check if input is inside a label
                if input_elem.find_parent('label'):
                    has_label = True
                
                if not has_label:
                    inputs_without_labels.append(input_elem)
            
            if not inputs:
                checks_passed += 1  # No form inputs
            elif not inputs_without_labels:
                checks_passed += 1
            else:
                issues.append(f"{len(inputs_without_labels)} form inputs missing labels")
            
            # Check 3: Proper heading hierarchy
            total_checks += 1
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            if not headings:
                # No headings is okay for some content
                checks_passed += 1
            else:
                heading_levels = [int(h.name[1]) for h in headings]
                has_h1 = 1 in heading_levels
                
                # Check hierarchy
                valid_hierarchy = True
                for i in range(1, len(heading_levels)):
                    if heading_levels[i] > heading_levels[i-1] + 1:
                        valid_hierarchy = False
                        break
                
                if has_h1 and valid_hierarchy:
                    checks_passed += 1
                else:
                    if not has_h1:
                        issues.append("Missing h1 heading")
                    if not valid_hierarchy:
                        issues.append("Heading hierarchy has gaps")
            
            # Check 4: Links have descriptive text
            total_checks += 1
            links = soup.find_all('a')
            links_without_text = []
            
            for link in links:
                text = link.get_text(strip=True)
                aria_label = link.get('aria-label', '')
                
                if not text and not aria_label:
                    links_without_text.append(link)
            
            if not links:
                checks_passed += 1
            elif not links_without_text:
                checks_passed += 1
            else:
                issues.append(f"{len(links_without_text)} links without descriptive text")
            
            # Check 5: Buttons have accessible names
            total_checks += 1
            buttons = soup.find_all('button')
            buttons_without_text = []
            
            for button in buttons:
                text = button.get_text(strip=True)
                aria_label = button.get('aria-label', '')
                
                if not text and not aria_label:
                    buttons_without_text.append(button)
            
            if not buttons:
                checks_passed += 1
            elif not buttons_without_text:
                checks_passed += 1
            else:
                issues.append(f"{len(buttons_without_text)} buttons without accessible names")
            
            # Calculate score
            score = checks_passed / total_checks if total_checks > 0 else 0.0
            
            details = {
                "checks_passed": checks_passed,
                "total_checks": total_checks,
                "issues": issues,
                "images_count": len(images),
                "images_without_alt": len(images_without_alt),
                "form_inputs_count": len(inputs),
                "inputs_without_labels": len(inputs_without_labels),
                "links_count": len(links),
                "links_without_text": len(links_without_text),
                "buttons_count": len(buttons),
                "buttons_without_text": len(buttons_without_text)
            }
            
            return {
                "score": score,
                "passed": score >= 0.7,  # 70% of checks must pass
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
