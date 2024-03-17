"""Run this script to launch the pipeline"""

import logging.config
import os
from datetime import datetime

from etl.master import run_etl


LOG_CONFIG = 'logging.conf'
CONFIG_DIR = os.getenv('CONFIG_DIR', '/app/config')
LOG_DIR = os.getenv('LOG_DIR', '/app/logs')
SQLALCHEMY_URL = os.getenv('SQLALCHEMY_URL')


def setup_logging():
    """Load logging configuration"""
    config_path = '/'.join([CONFIG_DIR, LOG_CONFIG])
    timestamp = datetime.now().strftime('%Y%m%d-%H:%M:%S')

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={'logfilename': f'{LOG_DIR}/{timestamp}.log'},
    )


if __name__ == '__main__':
    setup_logging()
    run_etl(SQLALCHEMY_URL)
