"""Configuration management for the harness."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class HarnessConfig:
    """Central configuration manager."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize configuration."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        
        # Load environment variables
        load_dotenv(self.project_root / ".env")
        
        # Load YAML configs
        self.prompts_config = self._load_yaml("prompts.yaml")
        self.evaluation_config = self._load_yaml("evaluation.yaml")
        self.agents_config = self._load_yaml("agents.yaml")
        
        # Setup paths
        self.prompts_dir = self.project_root / (os.getenv("PROMPTS_DIR", "prompts"))
        self.test_cases_dir = self.project_root / (os.getenv("TEST_CASES_DIR", "test_cases"))
        self.results_dir = self.project_root / (os.getenv("RESULTS_DIR", "results"))
        
        # Ensure directories exist
        self.prompts_dir.mkdir(exist_ok=True)
        self.test_cases_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        config_path = self.config_dir / filename
        if not config_path.exists():
            return {}
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def get_gemini_api_key(self) -> str:
        """Get Gemini API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        return api_key
    
    def get_gemini_model(self) -> str:
        """Get Gemini model name."""
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    def get_prompt_config(self, prompt_name: str) -> Dict[str, Any]:
        """Get configuration for a specific prompt."""
        prompts = self.prompts_config.get("prompts", {})
        if prompt_name not in prompts:
            raise ValueError(f"Prompt '{prompt_name}' not found in configuration")
        return prompts[prompt_name]
    
    def get_active_prompts(self) -> Dict[str, Dict[str, Any]]:
        """Get all active prompts."""
        prompts = self.prompts_config.get("prompts", {})
        return {name: config for name, config in prompts.items() if config.get("active", False)}
    
    def get_default_prompt(self) -> str:
        """Get the default prompt name."""
        strategy = self.prompts_config.get("strategy", {})
        return strategy.get("default_prompt", "base_v1")
    
    def get_evaluation_metrics(self) -> Dict[str, Any]:
        """Get evaluation metrics configuration."""
        return self.evaluation_config.get("metrics", {})
    
    def get_enabled_metrics(self) -> Dict[str, Any]:
        """Get only enabled evaluation metrics."""
        metrics = self.get_evaluation_metrics()
        return {name: config for name, config in metrics.items() if config.get("enabled", False)}
    
    def get_scoring_config(self) -> Dict[str, Any]:
        """Get scoring configuration."""
        return self.evaluation_config.get("scoring", {})
    
    def get_internal_agent_config(self) -> Dict[str, Any]:
        """Get internal agent (Gemini) configuration."""
        return self.agents_config.get("internal_agent", {})
    
    def get_external_agent_config(self) -> Dict[str, Any]:
        """Get external agent (Cursor) configuration."""
        return self.agents_config.get("external_agent", {})
    
    def get_shared_config(self) -> Dict[str, Any]:
        """Get shared agent configuration."""
        return self.agents_config.get("shared", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get_shared_config().get("logging", {})
    
    def get_caching_config(self) -> Dict[str, Any]:
        """Get caching configuration."""
        return self.get_shared_config().get("caching", {})


def load_config(project_root: Optional[Path] = None) -> HarnessConfig:
    """Load harness configuration."""
    return HarnessConfig(project_root)
