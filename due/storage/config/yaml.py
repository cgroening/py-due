from pathlib import Path
import yaml
from due.domain.models import Config
from due.storage.config.base import BaseConfigStorage


class YamlConfigStorage(BaseConfigStorage):
    _CONFIG_PATH = Path.home() / '.config' / 'due' / 'config.yaml'

    def load(self) -> Config:
        if not self._CONFIG_PATH.exists():
            return Config()

        try:
            with open(self._CONFIG_PATH, encoding='utf-8') as f:
                data: dict[str, object] = yaml.safe_load(f) or {}
            editor = data.get('editor', 'nvim')
            return Config(editor=str(editor))
        except Exception:
            return Config()
