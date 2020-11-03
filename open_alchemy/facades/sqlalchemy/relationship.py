"""Construct relationship properties."""

import typing

from sqlalchemy import orm

from open_alchemy import helpers
from open_alchemy.schemas.artifacts import types as artifacts_types

from . import types


def construct(
    *, artifacts: artifacts_types.TAnyRelationshipPropertyArtifacts
) -> types.Relationship:
    """
    Construct relationship from artifacts.

    Args:
        artifacts: The artifacts of the relationship.

    Returns:
        The SQLAlchemy relationship.

    """
    # Construct back reference
    backref = None
    if artifacts.backref_property is not None:
        # Calculate uselist
        uselist: typing.Optional[bool] = None
        if artifacts.sub_type == helpers.relationship.Type.ONE_TO_ONE:
            uselist = False

        backref = orm.backref(
            artifacts.backref_property,
            uselist=uselist,
        )

    # Calculate secondary
    secondary: typing.Optional[str] = None
    if artifacts.sub_type == helpers.relationship.Type.MANY_TO_MANY:
        secondary = artifacts.secondary

    # Construct kwargs
    kwargs: typing.Dict[str, typing.Any] = {}
    if artifacts.kwargs is not None:
        kwargs = artifacts.kwargs

    # Construct relationship
    return orm.relationship(
        artifacts.parent, backref=backref, secondary=secondary, **kwargs
    )
