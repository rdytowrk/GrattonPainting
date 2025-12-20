"""Analyze Tailwind CSS usage in HTML."""

import re
from typing import Dict, Any, Set
from bs4 import BeautifulSoup


class TailwindAnalyzer:
    """Analyzes Tailwind CSS class usage."""
    
    # Common Tailwind class prefixes
    TAILWIND_PREFIXES = {
        # Layout
        'container', 'box-', 'block', 'inline', 'flex', 'grid', 'hidden',
        # Spacing
        'p-', 'px-', 'py-', 'pt-', 'pr-', 'pb-', 'pl-',
        'm-', 'mx-', 'my-', 'mt-', 'mr-', 'mb-', 'ml-',
        'space-', 'gap-',
        # Sizing
        'w-', 'h-', 'min-w-', 'min-h-', 'max-w-', 'max-h-',
        # Typography
        'text-', 'font-', 'leading-', 'tracking-', 'antialiased',
        # Colors
        'bg-', 'text-', 'border-', 'ring-',
        # Borders
        'border', 'rounded', 'divide-',
        # Effects
        'shadow', 'opacity-', 'blur-',
        # Responsive
        'sm:', 'md:', 'lg:', 'xl:', '2xl:',
        # Flexbox/Grid
        'justify-', 'items-', 'content-', 'self-', 'order-',
        'col-', 'row-', 'auto-',
        # Position
        'static', 'fixed', 'absolute', 'relative', 'sticky',
        'top-', 'right-', 'bottom-', 'left-', 'inset-',
        # Display
        'visible', 'invisible',
        # Overflow
        'overflow-', 'truncate',
        # Transform
        'transform', 'translate-', 'rotate-', 'scale-', 'skew-',
        # Transitions
        'transition', 'duration-', 'ease-', 'delay-',
        # Interactivity
        'cursor-', 'pointer-events-', 'resize', 'select-',
        'hover:', 'focus:', 'active:', 'disabled:',
    }
    
    def __init__(self):
        """Initialize analyzer."""
        pass
    
    def is_tailwind_class(self, class_name: str) -> bool:
        """Check if a class name appears to be a Tailwind class."""
        # Check for direct matches
        if class_name in self.TAILWIND_PREFIXES:
            return True
        
        # Check for prefix matches
        for prefix in self.TAILWIND_PREFIXES:
            if class_name.startswith(prefix):
                return True
        
        # Check for responsive/state modifiers (e.g., md:text-lg, hover:bg-blue-500)
        if ':' in class_name:
            parts = class_name.split(':')
            if len(parts) == 2:
                modifier, base_class = parts
                # Check if modifier is valid
                valid_modifiers = ['sm', 'md', 'lg', 'xl', '2xl', 'hover', 'focus', 'active', 
                                   'disabled', 'group-hover', 'dark', 'first', 'last', 'even', 'odd']
                if modifier in valid_modifiers:
                    return self.is_tailwind_class(base_class)
        
        return False
    
    def analyze(self, html: str) -> Dict[str, Any]:
        """
        Analyze Tailwind CSS usage in HTML.
        
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
            
            all_classes: Set[str] = set()
            tailwind_classes: Set[str] = set()
            non_tailwind_classes: Set[str] = set()
            elements_with_classes = 0
            
            # Find all elements with class attributes
            for element in soup.find_all(class_=True):
                elements_with_classes += 1
                classes = element.get('class', [])
                
                for class_name in classes:
                    all_classes.add(class_name)
                    
                    if self.is_tailwind_class(class_name):
                        tailwind_classes.add(class_name)
                    else:
                        non_tailwind_classes.add(class_name)
            
            # Calculate coverage
            total_classes = len(all_classes)
            tailwind_count = len(tailwind_classes)
            
            if total_classes == 0:
                coverage = 0.0
            else:
                coverage = tailwind_count / total_classes
            
            # Score is based on coverage
            score = coverage
            
            # Check for common Tailwind patterns
            has_responsive = any(':' in c for c in tailwind_classes)
            has_spacing = any(c.startswith(('p-', 'm-', 'gap-', 'space-')) for c in tailwind_classes)
            has_colors = any(c.startswith(('bg-', 'text-')) and any(color in c for color in ['gray', 'blue', 'red', 'green', 'yellow', 'purple']) for c in tailwind_classes)
            
            details = {
                "total_classes": total_classes,
                "tailwind_classes_count": tailwind_count,
                "non_tailwind_classes_count": len(non_tailwind_classes),
                "coverage": coverage,
                "elements_with_classes": elements_with_classes,
                "has_responsive_classes": has_responsive,
                "has_spacing_classes": has_spacing,
                "has_color_classes": has_colors,
                "non_tailwind_classes": list(non_tailwind_classes)[:10]  # Sample
            }
            
            return {
                "score": score,
                "passed": coverage >= 0.7,  # 70% Tailwind coverage
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
