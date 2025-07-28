import argparse
import logging
import sys
from core.config_loader import load_config
from filler.form_filler import fill_form

# Logger setup
logger = logging.getLogger("CLI")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def parse_args():
    parser = argparse.ArgumentParser(description="Auto Form Filler CLI")
    parser.add_argument("--config", type=str, required=True, help="YAML config path")
    parser.add_argument("--dry-run", action="store_true", help="Run without making actual changes")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        config = load_config(args.config)
        fill_form(config, dry_run=args.dry_run, headless=args.headless)
    except Exception as e:
        logger.exception(f"Fatal error occurred: {e}")
    finally:
        logger.info("Execution completed.")
