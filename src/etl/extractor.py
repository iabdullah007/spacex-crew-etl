import logging
from typing import List

import requests


LOGGER = logging.getLogger(__name__)


class Extractor:
    def __init__(self):
        """
        This class extracts data from source file

        Args:
            in_file_path: path to the source file
        """
        self.spacex_crew_api_url = 'https://api.spacexdata.com/v4/crew'

    def extract_data(self) -> List[dict]:
        """
        Extracts data from CSV file

        Returns:
            data as a list of dictionaries
        """
        LOGGER.info('Starting data extraction job for crews')

        crews = []

        response = requests.get(self.spacex_crew_api_url)
        if response.status_code == 200:
            data = response.json()
            crews.extend(data)
            LOGGER.info(f'Successfully extracted crews: {len(crews)}')
        else:
            LOGGER.info(f'Failed to retrieve crews: {response.text}')

        return crews
