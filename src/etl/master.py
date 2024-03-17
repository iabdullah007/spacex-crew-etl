import logging

from .extractor import Extractor
from .loader import Loader
from .transformer import Transformer


LOGGER = logging.getLogger(__name__)


def run_etl(connection_url: str):
    """
    Runs whole ETL pipeline

    Args:
        input_file: path to the source file
        connection_url: the URL to an SQL database.
    """

    LOGGER.info('Started ETL job')

    extractor = Extractor()
    transformer = Transformer(extractor.extract_data())
    loader = Loader(transformer.transform_data(), connection_url)

    loader.load_data()

    LOGGER.info('Finished ETL job')
