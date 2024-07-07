import logging
import os
from uvicorn.config import LOGGING_CONFIG as uvicorn_log_config

logs_root_path="../logs"
os.makedirs(logs_root_path, exist_ok=True)

# default log formatter
log_formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s \"%(message)s\"",
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configure logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

file_handler = logging.FileHandler(f"{logs_root_path}/app.log")
file_handler.setFormatter(log_formatter)



# Uvicorn stream logging configuration
uvicorn_log_config['formatters']['default']['fmt'] = log_formatter._fmt
uvicorn_log_config['formatters']['default']['datefmt'] = log_formatter.datefmt

# file handler for Uvicorn logs
uvicorn_file_handler = logging.FileHandler(f"{logs_root_path}/uvicorn.log")
uvicorn_file_handler.setFormatter(log_formatter)
logging.getLogger("uvicorn").addHandler(uvicorn_file_handler)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler, uvicorn_file_handler]
)