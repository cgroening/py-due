from pathlib import Path
import pytest
from due.domain.models import Config
from due.storage.config.yaml import YamlConfigStorage


@pytest.fixture
def storage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> YamlConfigStorage:
    monkeypatch.setattr(
        YamlConfigStorage, '_CONFIG_PATH', tmp_path / 'config.yaml'
    )
    return YamlConfigStorage()


class TestLoad:
    def test_loads_editor_from_yaml(
        self, storage: YamlConfigStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'config.yaml').write_text('editor: emacs\n')
        assert storage.load().editor == 'emacs'

    def test_returns_default_editor_when_file_missing(
        self, storage: YamlConfigStorage
    ) -> None:
        assert storage.load().editor == 'nvim'

    def test_returns_default_editor_on_invalid_yaml(
        self, storage: YamlConfigStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'config.yaml').write_text(': invalid: {')
        assert storage.load().editor == 'nvim'

    def test_returns_default_editor_when_key_absent(
        self, storage: YamlConfigStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'config.yaml').write_text('other_key: value\n')
        assert storage.load().editor == 'nvim'

    def test_returns_config_instance(
        self, storage: YamlConfigStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'config.yaml').write_text('editor: vim\n')
        assert isinstance(storage.load(), Config)
