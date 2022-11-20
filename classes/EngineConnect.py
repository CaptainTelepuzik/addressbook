from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Config.common import SQLALCHEMY_DATABASE_URI

class EngineConnect:
    _engine = None
    _session = None

    def __init__(self):
        self._engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self._engine.connect()
        self._session = sessionmaker(bind=self._engine)()

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session