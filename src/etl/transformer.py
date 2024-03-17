import logging
from typing import List, Optional

from pydantic import ValidationError

from .models import CrewModel


LOGGER = logging.getLogger(__name__)


class Transformer:
    def __init__(self, raw_data: List[dict]):
        """
        This class transforms extracted data according to the desired model

        Args:
            raw_data: extracted data
        """
        self.raw_data = raw_data

    def transform_data(self) -> List[CrewModel]:
        """
        Transforms data

        Returns:
            transformed data as a list of models
        """
        return list(filter(bool, map(self.transform_single_item, self.raw_data)))

    def transform_single_item(self, input_item: dict) -> Optional[CrewModel]:
        """
        Transforms single item of extracted data

        Args:
            input_item: part of extracted data

        Returns:
            model if transformation was successful
        """
        transformed = None

        try:
            transformed = CrewModel(**input_item)
        except ValidationError as ex:
            print(f'Failed validation for {input_item}: {ex.errors()[0]}')

        return transformed
