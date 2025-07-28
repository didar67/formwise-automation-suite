import pytest
from filler.form_filler import fill_form
from core.config_loader import load_config

def test_fill_form_dry_run():
    config = load_config("config/config.yaml")
    try:
        fill_form(config, dry_run=True, headless=True)
    except Exception as e:
        pytest.fail(f"Dry run failed unexpectedly: {e}")