import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import dialect, insert
from sqlalchemy.orm import Session, sessionmaker

from .models import CrewModel, CrewSqlalchemyOrm


LOGGER = logging.getLogger(__name__)


def connect(connection_url: str) -> Session:
    """
    Connects to the database and returns a Session object.

    Args:
        connection_url: the URL to an SQL database.
    """
    Session = sessionmaker()
    Session.configure(bind=create_engine(connection_url, echo=True))
    LOGGER.info('Successfully created database session')
    return Session()


class Loader:
    def __init__(self, crew_data: List[CrewModel], connection_url: str):
        """
        This class loads transformed data into the database

        Args:
            crew_data: transformed data
            connection_url: the URL to an SQL database.
        """
        self.session = connect(connection_url)
        self.crew_data = crew_data

    def load_data(self):
        """
        Inserts data into the database
        """
        LOGGER.info('Starting data loading job to load crews to Postgres DB')

        statement = self._prepare_upsert_statement()

        LOGGER.info(self._compile_query(statement))

        self.session.execute(statement)
        self.session.commit()

        LOGGER.info(f'Successfully loaded crews: {len(self.crew_data)}')

    def _prepare_upsert_statement(self):
        """Prepares and returns an upsert statement (insert if not present, update if present based on `id`)"""

        table = CrewSqlalchemyOrm.__table__
        all_rows = list(map(lambda x: x.dict(), self.crew_data))

        update_cols = [
            c.name for c in table.c if c not in list(
                table.primary_key.columns,
            )
        ]

        statement = insert(table).values(all_rows)
        on_conflict_statement = statement.on_conflict_do_update(
            index_elements=table.primary_key.columns,
            set_={k: getattr(statement.excluded, k) for k in update_cols},
        )
        return on_conflict_statement

    def _compile_query(self, query):
        """Compiles the given insert query and returns stringified version"""

        compiler = query.compile if 'statement' not in query else query.statement.compile
        return compiler(dialect=dialect())
