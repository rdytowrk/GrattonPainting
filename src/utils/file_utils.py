"""File utility functions."""

import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, file_path: Path, pretty: bool = True):
    """Save data as JSON."""
    ensure_dir(file_path.parent)
    
    with open(file_path, 'w') as f:
        if pretty:
            json.dump(data, f, indent=2, cls=DateTimeEncoder)
        else:
            json.dump(data, f, cls=DateTimeEncoder)


def load_json(file_path: Path) -> Any:
    """Load JSON from file."""
    if not file_path.exists():
        return None
    
    with open(file_path, 'r') as f:
        return json.load(f)


def save_html(html: str, file_path: Path):
    """Save HTML to file."""
    ensure_dir(file_path.parent)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)


def load_html(file_path: Path) -> str:
    """Load HTML from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
