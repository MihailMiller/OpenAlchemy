"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""
# pylint: disable=no-member,super-init-not-called,unused-argument

import typing

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import models


class EmployeeDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]
    division: typing.Optional[str]


class TEmployee(typing.Protocol):
    """SQLAlchemy model protocol."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: typing.Optional[int]
    name: typing.Optional[str]
    division: typing.Optional[str]

    def __init__(
        self,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        division: typing.Optional[str] = None,
    ) -> None:
        """Construct."""
        ...

    @classmethod
    def from_dict(
        cls,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        division: typing.Optional[str] = None,
    ) -> "TEmployee":
        """Construct from a dictionary (eg. a POST payload)."""
        ...

    @classmethod
    def from_str(cls, value: str) -> "TEmployee":
        """Construct from a JSON string (eg. a POST payload)."""
        ...

    def to_dict(self) -> EmployeeDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        ...

    def to_str(self) -> str:
        """Convert to a JSON string (eg. to send back for a GET request)."""
        ...


Employee: TEmployee = models.Employee  # type: ignore
