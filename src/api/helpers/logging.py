from logging import getLogger
from os import getenv

"""
Logging Levels:
  - Info
  - Warning
  - Debug
  - Error
"""

LOG_LEVEL = getenv('API_LOG_LEVEL')

logger = getLogger("uvicorn.error")
logger.setLevel(LOG_LEVEL)
logger.info(f'Log Level set to {LOG_LEVEL}')