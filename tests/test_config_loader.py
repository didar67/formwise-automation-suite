import pytest
from core.config_loader import load_config, FormConfig
import os

def test_valid_config_load():
    test_path = "config/config.yaml"
    config = load_config(test_path)
    assert isinstance(config, FormConfig)
    assert str(config.url).startswith("http")
    assert len(config.fields) > 0
    assert config.submit_button is not None

def test_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        load_config("config/missing.yaml")