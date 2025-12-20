"""Gemini API integration for HTML conversion."""

import time
import re
from pathlib import Path
from typing import Optional, Dict, Any
from google import genai

from ..harness.config import HarnessConfig
from ..harness.models import ConversionResult


class GeminiAgent:
    """Agent that uses Google Gemini API for HTML conversion."""
    
    def __init__(self, config: HarnessConfig):
        """Initialize Gemini agent."""
        self.config = config
        
        # Get API key and configuration
        api_key = config.get_gemini_api_key()
        agent_config = config.get_internal_agent_config()
        self.model_name = agent_config.get("model", config.get_gemini_model())
        self.generation_config = agent_config.get("generation", {})
        self.api_config = agent_config.get("api", {})
        self.response_config = agent_config.get("response", {})
        
        # Initialize Gemini client with new API
        self.client = genai.Client(api_key=api_key)
        
        # Cost tracking (approximate rates for Gemini 1.5 Flash)
        # Free tier: 15 RPM, 1M TPM, 1.5K RPD
        self.input_cost_per_1k = 0.0  # Free tier
        self.output_cost_per_1k = 0.0  # Free tier
    
    def _get_generation_config(self, override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get generation configuration with optional overrides."""
        config = {
            "temperature": self.generation_config.get("temperature", 0.7),
            "top_p": self.generation_config.get("top_p", 0.95),
            "top_k": self.generation_config.get("top_k", 40),
            "max_output_tokens": self.generation_config.get("max_output_tokens", 8000),
        }
        
        if override:
            config.update(override)
        
        return config
    
    def load_prompt(self, prompt_name: str) -> str:
        """Load prompt template from file."""
        prompt_config = self.config.get_prompt_config(prompt_name)
        prompt_file = self.config.prompts_dir / prompt_config["file"]
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r') as f:
            return f.read()
    
    def prepare_prompt(self, prompt_template: str, input_html: str) -> str:
        """Prepare the final prompt by inserting input HTML."""
        # Replace placeholder with actual HTML
        return prompt_template.replace("{input_html}", input_html)
    
    def extract_html_from_response(self, response_text: str) -> str:
        """Extract HTML code from the response."""
        if not self.response_config.get("extract_code_blocks", True):
            return response_text
        
        # Try to extract HTML from markdown code blocks
        html_pattern = r"```html\s*(.*?)\s*```"
        matches = re.findall(html_pattern, response_text, re.DOTALL)
        
        if matches:
            # Return the first HTML code block found
            return matches[0].strip()
        
        # Try generic code blocks
        code_pattern = r"```\s*(.*?)\s*```"
        matches = re.findall(code_pattern, response_text, re.DOTALL)
        
        if matches:
            # Return the first code block that looks like HTML
            for match in matches:
                if "<" in match and ">" in match:
                    return match.strip()
        
        # If no code blocks, return the entire response
        return response_text.strip()
    
    def convert_html(
        self,
        test_case_id: str,
        prompt_name: str,
        input_html: str,
        generation_override: Optional[Dict[str, Any]] = None
    ) -> ConversionResult:
        """
        Convert HTML using the specified prompt.
        
        Args:
            test_case_id: ID of the test case
            prompt_name: Name of the prompt to use
            input_html: Input HTML to convert
            generation_override: Optional generation config overrides
            
        Returns:
            ConversionResult with the conversion output and metadata
        """
        start_time = time.time()
        
        try:
            # Load and prepare prompt
            prompt_template = self.load_prompt(prompt_name)
            full_prompt = self.prepare_prompt(prompt_template, input_html)
            
            # Get generation config
            gen_config = self._get_generation_config(generation_override)
            
            # Generate response with retry logic
            max_retries = self.api_config.get("retry_attempts", 3)
            retry_delay = self.api_config.get("retry_delay", 2)
            
            response = None
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=full_prompt,
                        config=genai.types.GenerateContentConfig(
                            temperature=gen_config.get("temperature", 0.7),
                            top_p=gen_config.get("top_p", 0.95),
                            top_k=gen_config.get("top_k", 40),
                            max_output_tokens=gen_config.get("max_output_tokens", 8000),
                        )
                    )
                    break
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    continue
            
            if response is None:
                raise last_error or Exception("Failed to generate response")
            
            # Extract response text
            response_text = response.text
            
            # Extract HTML from response
            output_html = self.extract_html_from_response(response_text)
            
            # Calculate metrics
            response_time = time.time() - start_time
            
            # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
            input_tokens = len(full_prompt) // 4
            output_tokens = len(response_text) // 4
            total_tokens = input_tokens + output_tokens
            
            # Calculate cost
            input_cost = (input_tokens / 1000) * self.input_cost_per_1k
            output_cost = (output_tokens / 1000) * self.output_cost_per_1k
            total_cost = input_cost + output_cost
            
            # Create result
            result = ConversionResult(
                test_case_id=test_case_id,
                prompt_name=prompt_name,
                output_html=output_html,
                raw_response=response_text if self.response_config.get("save_raw_response", True) else None,
                success=True,
                tokens_used=total_tokens,
                response_time=response_time,
                cost=total_cost,
                output_size=len(output_html),
                line_count=len(output_html.split('\n'))
            )
            
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            
            return ConversionResult(
                test_case_id=test_case_id,
                prompt_name=prompt_name,
                output_html="",
                success=False,
                error_message=str(e),
                response_time=response_time
            )
    
    def test_connection(self) -> bool:
        """Test if the API connection is working."""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hello, respond with 'OK'"
            )
            return bool(response.text)
        except Exception:
            return False
