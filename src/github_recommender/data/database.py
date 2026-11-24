# src/github_recommender/data/database.py

from __future__ import annotations

import logging
from typing import Self
from types import TracebackType
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.github_recommender.config.settings import Settings


logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(
        self,
        settings: Settings,
    ) -> None:
        self._settings = settings
        self._engine: Engine | None = None

    @property
    def engine(self) -> Engine: 
        """Return the intialized SQLAlchemy engine."""
        if self._engine is None:
            raise RuntimeError(
                "PostgreSQL engine is not intialized. "
                "Call connect() first."
            )
        
        return self._engine

    def connect(self) -> Self:
        """Create the engine and verify database connectivity.""" 
        if self._engine is not None:
            return self  

        engine = create_engine(
            self._settings.database.dsn,
            pool_pre_ping=True,
            pool_size=self._settings.database.pool_size,
            pool_recycle=self._settings.database.pool_recycle,
            pool_timeout=self._settings.database.pool_timeout,
            max_overflow=self._settings.database.max_overflow,
            echo=self._settings.log_level.upper() == "DEBUG",
        ) 

        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

        except Exception:
            engine.dispose()  
            logger.exception(
                "Failed to initialize PostgreSQL connectivity."
            )    
            raise

        self._engine = engine

        logger.info("PostgreSQL connection established.")

        return self

    def health_check(self) -> bool:
        """Return whether PostgreSQL is reachable."""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return True

        except SQLAlchemyError:
            logger.exception("PostgreSQL health check failed.")
            return False

    def close(self) -> None:
        """Dispose of the connection pool and release resources."""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

            logger.info("PostgreSQL connection pool closed.")

    def __enter__(self) -> Self:
        """Initialize connectivity when entering a context."""
        return self.connect()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Release resources when leaving a context."""
        self.close()
