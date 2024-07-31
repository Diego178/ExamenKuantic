import logging
import logging.config
import logging.handlers
import pathlib
import json
import os

logger = logging.getLogger("movies_app")

def setup_logging():
    log_dir = pathlib.Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    config_file = pathlib.Path(os.path.dirname(__file__)) / "config.json"
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)
    logger = logging.getLogger("movies_app")
    

