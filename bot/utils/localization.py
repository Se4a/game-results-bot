import json
import os
from pathlib import Path

class Localization:
    def __init__(self):
        self.locales_path = Path(__file__).parent.parent / 'locales'
        self.locales = {}
        self.load_locales()
    
    def load_locales(self):
        """Load all locale files"""
        for file_path in self.locales_path.glob('*.json'):
            lang = file_path.stem
            with open(file_path, 'r', encoding='utf-8') as f:
                self.locales[lang] = json.load(f)
    
    def get_text(self, key: str, lang: str = 'en') -> str:
        """Get localized text by key"""
        if lang not in self.locales:
            lang = 'en'
        
        # Navigate through nested keys (key can be like 'menu.csgo')
        keys = key.split('.')
        value = self.locales[lang]
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return f"[{key}]"  # Key not found
        
        return value
    
    def get_all_languages(self) -> list:
        """Get list of available languages"""
        return list(self.locales.keys())

# Singleton instance
_localization = Localization()

def get_text(key: str, lang: str = 'en') -> str:
    return _localization.get_text(key, lang)