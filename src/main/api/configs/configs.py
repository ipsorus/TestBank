import os
from pathlib import Path
from typing import Any


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._dictionary = {}

            config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(f'Config path not found: {config_path}')

            with open(config_path, 'r') as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped or stripped.startswith('#'):
                        continue
                    if '=' in stripped:
                        key, value = stripped.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        cls._instance._dictionary[key] = os.getenv(key, value)

        return cls._instance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        return Config()._dictionary.get(key, default_value)