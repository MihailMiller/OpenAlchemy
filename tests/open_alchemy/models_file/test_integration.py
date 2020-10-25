"""Tests for models file from artifacts."""

# pylint: disable=line-too-long

import sys

import pytest
from mypy import api

from open_alchemy import helpers as oa_helpers
from open_alchemy import models_file
from open_alchemy.schemas import artifacts as schemas_artifacts

_DOCSTRING = '"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""'
_EXPECTED_TD_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_TD_BASE = "typing_extensions.TypedDict"
_EXPECTED_MODEL_BASE = "typing.Protocol"
if sys.version_info[1] < 8:
    _EXPECTED_MODEL_BASE = "typing_extensions.Protocol"
_ADDITIONAL_IMPORT = ""
if sys.version_info[1] < 8:
    _ADDITIONAL_IMPORT = """
import typing_extensions"""


def _construct_model_artifacts(properties):
    """Construct model artifacts"""
    return schemas_artifacts.types.ModelArtifacts(
        tablename="tablename",
        inherits=None,
        parent=None,
        description=None,
        mixins=None,
        kwargs=None,
        composite_index=None,
        composite_unique=None,
        backrefs=[],
        properties=properties,
    )


def _construct_simple_property_artifacts(type_, nullable):
    """Construct the artifacts for a simple property."""
    return schemas_artifacts.types.SimplePropertyArtifacts(
        type=oa_helpers.property_.Type.SIMPLE,
        open_api=schemas_artifacts.types.OpenApiSimplePropertyArtifacts(
            type=type_,
            format=None,
            max_length=None,
            nullable=nullable,
            default=None,
            read_only=None,
            write_only=None,
        ),
        extension=schemas_artifacts.types.ExtensionSimplePropertyArtifacts(
            primary_key=False,
            autoincrement=None,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=None,
        ),
        schema={"type": type_},
        required=False,
        description=None,
    )


def _construct_relationship_property_artifacts():
    """Construct the artifacts for a relationship property."""
    return schemas_artifacts.types.ManyToOneRelationshipPropertyArtifacts(
        type=oa_helpers.property_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=None,
    )


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        pytest.param(
            [
                (
                    "Model",
                    _construct_model_artifacts(
                        [
                            (
                                "id",
                                _construct_simple_property_artifacts(
                                    type_="integer", nullable=None
                                ),
                            )
                        ]
                    ),
                )
            ],
            f'''{_DOCSTRING}
# pylint: disable=no-member,super-init-not-called,unused-argument

import typing

import sqlalchemy{_ADDITIONAL_IMPORT}
from sqlalchemy import orm

from open_alchemy import models

Base = models.Base  # type: ignore


class ModelDict({_EXPECTED_TD_BASE}, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]


class TModel({_EXPECTED_MODEL_BASE}):
    """
    SQLAlchemy model protocol.

    Attrs:
        id: The id of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: 'sqlalchemy.Column[typing.Optional[int]]'

    def __init__(self, id: typing.Optional[int] = None) -> None:
        """
        Construct.

        Args:
            id: The id of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[int] = None) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: The id of the Model.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TModel":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> ModelDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Model: typing.Type[TModel] = models.Model  # type: ignore
''',
            id="single",
        ),
        pytest.param(
            [
                (
                    "Model1",
                    _construct_model_artifacts(
                        [
                            (
                                "id",
                                _construct_simple_property_artifacts(
                                    type_="integer", nullable=None
                                ),
                            )
                        ]
                    ),
                ),
                (
                    "Model2",
                    _construct_model_artifacts(
                        [
                            (
                                "id",
                                _construct_simple_property_artifacts(
                                    type_="string", nullable=None
                                ),
                            )
                        ]
                    ),
                ),
            ],
            f'''{_DOCSTRING}
# pylint: disable=no-member,super-init-not-called,unused-argument

import typing

import sqlalchemy{_ADDITIONAL_IMPORT}
from sqlalchemy import orm

from open_alchemy import models

Base = models.Base  # type: ignore


class Model1Dict({_EXPECTED_TD_BASE}, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]


class TModel1({_EXPECTED_MODEL_BASE}):
    """
    SQLAlchemy model protocol.

    Attrs:
        id: The id of the Model1.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: 'sqlalchemy.Column[typing.Optional[int]]'

    def __init__(self, id: typing.Optional[int] = None) -> None:
        """
        Construct.

        Args:
            id: The id of the Model1.

        """
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[int] = None) -> "TModel1":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: The id of the Model1.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TModel1":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> Model1Dict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Model1: typing.Type[TModel1] = models.Model1  # type: ignore


class Model2Dict({_EXPECTED_TD_BASE}, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[str]


class TModel2({_EXPECTED_MODEL_BASE}):
    """
    SQLAlchemy model protocol.

    Attrs:
        id: The id of the Model2.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: 'sqlalchemy.Column[typing.Optional[str]]'

    def __init__(self, id: typing.Optional[str] = None) -> None:
        """
        Construct.

        Args:
            id: The id of the Model2.

        """
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[str] = None) -> "TModel2":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: The id of the Model2.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TModel2":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> Model2Dict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Model2: typing.Type[TModel2] = models.Model2  # type: ignore
''',
            id="multiple",
        ),
    ],
)
@pytest.mark.models_file
def test_integration(artifacts, expected_source):
    """
    GIVEN schema and name
    WHEN schema is added to the models file and the models file is generated
    THEN the models source code is returned.
    """
    source = models_file.generate(artifacts=artifacts)

    assert source == expected_source


def _create_source_file(source, tmp_path):
    """Create a file with the source code."""
    directory = tmp_path / "models"
    directory.mkdir()
    source_file = directory / "models.py"
    source_file.write_text(source)
    return source_file


@pytest.mark.parametrize(
    "artifacts",
    [
        pytest.param(
            [
                (
                    "Model",
                    _construct_model_artifacts(
                        [
                            (
                                "id",
                                _construct_simple_property_artifacts(
                                    type_="integer", nullable=None
                                ),
                            )
                        ]
                    ),
                )
            ],
            id="simple",
        ),
        pytest.param(
            [
                (
                    "RefModel",
                    _construct_model_artifacts(
                        [
                            (
                                "id",
                                _construct_simple_property_artifacts(
                                    type_="integer", nullable=None
                                ),
                            )
                        ]
                    ),
                ),
                (
                    "Model",
                    _construct_model_artifacts(
                        [("model", _construct_relationship_property_artifacts())]
                    ),
                ),
            ],
            id="relationship",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.slow
def test_generate_type_return(tmp_path, artifacts):
    """
    GIVEN schema
    WHEN the models file is generated and mypy is run over it
    THEN no errors are returned.
    """
    source = models_file.generate(artifacts=artifacts)
    source_file = _create_source_file(source, tmp_path)

    normal_report, error_report, returncode = api.run([str(source_file)])

    if returncode > 0:
        if normal_report:
            print("\nType checking report:\n")  # allow-print
            print(normal_report)  # stdout allow-print

        if error_report:
            print("\nError report:\n")  # allow-print
            print(error_report)  # stderr allow-print

    assert returncode == 0


@pytest.mark.parametrize(
    "artifacts, mypy_check, expected_out_substr",
    [
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "id",
                        _construct_simple_property_artifacts(
                            type_="integer", nullable=None
                        ),
                    )
                ]
            ),
            "reveal_type(Model.id)",
            "'sqlalchemy.sql.schema.Column[Union[builtins.int, None]]'",
            id="nullable column",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "id",
                        _construct_simple_property_artifacts(
                            type_="integer", nullable=None
                        ),
                    )
                ]
            ),
            "model = Model()\nreveal_type(model.id)",
            "'Union[builtins.int, None]'",
            id="nullable column instance",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "id",
                        _construct_simple_property_artifacts(
                            type_="integer", nullable=False
                        ),
                    )
                ]
            ),
            "reveal_type(Model.id)",
            "'sqlalchemy.sql.schema.Column[builtins.int*]'",
            id="not nullable column",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.slow
def test_generate_type_check(tmp_path, artifacts, mypy_check, expected_out_substr):
    """
    GIVEN schema, a mypy check and expected mypy output substring
    WHEN the models file is generated and mypy is run over it
    THEN the expected output substring is in the mypy output.
    """
    source = models_file.generate(artifacts=[("Model", artifacts)]) + f"\n{mypy_check}"
    source_file = _create_source_file(source, tmp_path)

    out, _, _ = api.run([str(source_file)])

    assert expected_out_substr in out
