"""Tests for type_."""
# pylint: disable=protected-access,unused-import

import datetime
import sys
import typing

import pytest
import sqlalchemy
import typeguard
from sqlalchemy.ext import declarative

import open_alchemy
from open_alchemy import helpers
from open_alchemy import models_file
from open_alchemy import types
from open_alchemy.column_factory import object_ref


@pytest.mark.parametrize(
    "type_, format_, nullable, required, generated, de_ref, expected_type",
    [
        ("integer", None, False, None, None, None, "int"),
        ("integer", "int32", False, None, None, None, "int"),
        ("integer", "int64", False, None, None, None, "int"),
        ("number", None, False, None, None, None, "float"),
        ("number", "float", False, None, None, None, "float"),
        ("string", None, False, None, None, None, "str"),
        ("string", "password", False, None, None, None, "str"),
        ("string", "byte", False, None, None, None, "str"),
        ("string", "binary", False, None, None, None, "bytes"),
        ("string", "date", False, None, None, None, "datetime.date"),
        ("string", "date-time", False, None, None, None, "datetime.datetime"),
        ("boolean", None, False, None, None, None, "bool"),
        ("object", None, False, None, None, "RefModel", '"RefModel"'),
        ("array", None, None, None, None, "RefModel", 'typing.Sequence["RefModel"]'),
        ("integer", None, None, None, None, None, "typing.Optional[int]"),
        ("integer", None, None, True, None, None, "int"),
        ("integer", None, None, None, True, None, "int"),
        ("integer", None, None, None, False, None, "typing.Optional[int]"),
    ],
    ids=[
        "integer no format",
        "integer int32 format",
        "integer int64 format",
        "number no format",
        "number float format",
        "string no format",
        "string password format",
        "string byte format",
        "string binary format",
        "string date format",
        "string date-time format",
        "boolean no format",
        "object",
        "array",
        "nullable and required None",
        "nullable None required True",
        "nullable None generated True",
        "nullable None generated False",
    ],
)
@pytest.mark.models_file
def test_model(type_, format_, nullable, required, generated, de_ref, expected_type):
    """
    GIVEN type, format, nullable and required
    WHEN model is called with the type, format, nullable and required
    THEN the expected type is returned.
    """
    artifacts = models_file.types.ColumnSchemaArtifacts(
        type=type_,
        format=format_,
        nullable=nullable,
        required=required,
        de_ref=de_ref,
        generated=generated,
    )

    returned_type = models_file._model._type.model(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        ("integer", "int"),
        ("object", '"RefModelDict"'),
        ("array", 'typing.Sequence["RefModelDict"]'),
    ],
    ids=["plain", "object", "array"],
)
@pytest.mark.models_file
def test_dict(type_, expected_type):
    """
    GIVEN None format and required, False nullable and de_ref and given type
    WHEN typed_dict is called with the type, format, nullable, required and de_ref
    THEN the given expected type is returned.
    """
    artifacts = models_file.types.ColumnSchemaArtifacts(
        type=type_, nullable=False, de_ref="RefModel"
    )

    returned_type = models_file._model._type.typed_dict(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "type_, format_, nullable, required, generated, value",
    [
        ("integer", None, None, None, None, 1),
        ("integer", "int32", None, None, None, 1),
        ("integer", "int64", None, None, None, 1),
        ("number", None, None, None, None, 1.0),
        ("number", "float", None, None, None, 1.0),
        ("string", None, None, None, None, "value 1"),
        ("string", "password", None, None, None, "value 1"),
        ("string", "byte", None, None, None, "value 1"),
        ("string", "binary", None, None, None, b"value 1"),
        ("string", "date", None, None, None, datetime.date(year=2000, month=1, day=1)),
        (
            "string",
            "date-time",
            None,
            None,
            None,
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
        ),
        ("boolean", None, None, None, None, True),
        # nullable
        ("integer", None, None, None, None, 1),
        ("integer", None, None, None, None, None),
        ("integer", None, True, None, None, 1),
        ("integer", None, True, None, None, None),
        ("integer", None, False, None, None, 1),
        # required
        ("integer", None, None, None, None, 1),
        ("integer", None, None, None, None, None),
        ("integer", None, None, True, None, 1),
        ("integer", None, None, False, None, 1),
        ("integer", None, None, False, None, None),
        # generated
        ("integer", None, None, None, None, 1),
        ("integer", None, None, None, None, None),
        ("integer", None, None, None, True, 1),
        ("integer", None, None, None, False, 1),
        ("integer", None, None, None, False, None),
    ],
    ids=[
        "type integer format None      value int",
        "type integer format int32     value int",
        "type integer format int64     value int",
        "type number  format None      value float",
        "type number  format double    value float",
        "type string  format None      value str",
        "type string  format password  value str",
        "type string  format byte      value str",
        "type string  format binary    value bytes",
        "type string  format date      value datetime.date",
        "type string  format date-time value datetime.datetime",
        "type boolean format None      value bool",
        "nullable None  value not None",
        "nullable None  value None",
        "nullable True  value not None",
        "nullable True  value None",
        "nullable False value not None",
        "required None  value not None",
        "required None  value None",
        "required True  value not None",
        "required False value not None",
        "required False value None",
        "generated None  value not None",
        "generated None  value None",
        "generated True  value not None",
        "generated False value not None",
        "generated False value None",
    ],
)
@pytest.mark.models_file
def test_model_database_type_simple(
    engine, sessionmaker, type_, format_, nullable, required, generated, value
):
    """
    GIVEN simple type, format, nullable, required, generated and a value
    WHEN a specification is written for the combination and a model created and
        initialized with the value
    THEN the queried value complies with the type calculated by type_.model.
    """
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": True,
                        },
                        "column": {
                            "type": type_,
                            "format": format_,
                            "nullable": nullable,
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                    # Use required to implement generated
                    "required": ["column"] if required or generated else [],
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Create artifacts
    artifacts = models_file.types.ColumnSchemaArtifacts(
        type=type_, format=format_, nullable=nullable, required=required
    )
    calculated_type_str = models_file._model._type.model(artifacts=artifacts)
    calculated_type = eval(calculated_type_str)  # pylint: disable=eval-used

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value
    typeguard.check_type("queried_model.column", queried_model.column, calculated_type)


@pytest.mark.parametrize(
    "nullable, required, generated",
    [(False, None, None), (None, True, None), (None, None, True)],
    ids=[
        "nullable False value not None",
        "required False value None",
        "generated False value None",
    ],
)
@pytest.mark.models_file
def test_model_database_type_simple_nullable_fail(
    engine, sessionmaker, nullable, required, generated
):
    """
    GIVEN simple type, format, nullable, required, generated and a None value
    WHEN a specification is written for the combination and a model created and
        initialized with the value
    THEN sqlalchemy.exc.IntegrityError is raised.
    """
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": True,
                        },
                        "column": {"type": "integer", "nullable": nullable},
                    },
                    "x-tablename": "table",
                    "type": "object",
                    # Use required to implement generated
                    "required": ["column"] if required or generated else [],
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(column=None)
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.flush()


@pytest.mark.models_file
def test_model_database_type_many_to_one(engine, sessionmaker):
    """
    GIVEN spec for a many to one relationship
    WHEN spec is constructed with model factory and queried
    THEN the referenced type is a single object that is nullable and the back reference
        is an array that is not nullable.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "RefTable": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                    },
                    "x-tablename": "ref_table",
                    "x-backref": "tables",
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_table": {"$ref": "#/components/schemas/RefTable"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")
    ref_model = model_factory(name="RefTable")

    # Calculate the type through model factory operations
    artifacts = types.ObjectArtifacts(
        spec={},
        fk_column="id",
        relationship=types.RelationshipArtifacts(
            model_name="RefTable",
            back_reference=types.BackReferenceArtifacts(property_name="table"),
        ),
    )
    schema = object_ref._schema.calculate(artifacts=artifacts)
    backref_schema = helpers.backref._calculate_schema(
        artifacts=artifacts, ref_from_array=False, model_name="Table"
    )
    model_artifacts = models_file._model._artifacts.gather_column_artifacts(
        schema=schema, required=None
    )
    model_backref_artifacts = models_file._model._artifacts.gather_column_artifacts(
        schema=backref_schema, required=None
    )
    calculated_type_str = models_file._model._type.model(artifacts=model_artifacts)
    calculated_backref_type_str = models_file._model._type.model(
        artifacts=model_backref_artifacts
    )

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    ref_model_instance1 = ref_model(id=11, name="ref table name 1")
    model_instance1 = model(id=12, name="table name 1", ref_table=ref_model_instance1)
    session = sessionmaker()
    session.add(ref_model_instance1)
    session.add(model_instance1)
    session.flush()
    # Creating instance of model with None ref_model
    model_instance2 = model(id=22, name="table name 2", ref_table=None)
    session.add(model_instance2)
    session.flush()

    # Querying session
    queried_models = session.query(model).all()
    assert queried_models[0].ref_table is not None
    assert queried_models[1].ref_table is None

    # Check that returned type is correct
    assert calculated_type_str == 'typing.Optional["RefTable"]'

    # Creating instance of ref_model without models
    ref_model_instance2 = ref_model(id=21, name="ref table name 2")
    session.add(ref_model_instance2)
    # Creating instance of ref_model without empty models
    ref_model_instance3 = ref_model(id=31, name="ref table name 3", tables=[])
    session.add(ref_model_instance3)
    # Creating instance of ref_model without single model
    ref_model_instance4 = ref_model(
        id=41, name="ref table name 4", tables=[model(id=42, name="table name 4")]
    )
    session.add(ref_model_instance4)
    session.flush()

    # Querying session
    queried_ref_models = session.query(ref_model).all()
    assert len(queried_ref_models[1].tables) == 0
    assert len(queried_ref_models[2].tables) == 0
    assert len(queried_ref_models[3].tables) == 1

    assert calculated_backref_type_str == 'typing.Sequence["Table"]'

    # Try constructing null for models
    with pytest.raises(TypeError):
        ref_model(id=41, name="ref table name 4", tables=None)


@pytest.mark.models_file
def test_model_database_type_many_to_one_not_nullable(engine, sessionmaker):
    """
    GIVEN spec with many to one relationship that is not nullable
    WHEN models are constructed and None is passed for the object reference
    THEN sqlalchemy.exc.IntegrityError is raised.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "RefTable": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                    },
                    "x-tablename": "ref_table",
                    "x-backref": "tables",
                    "type": "object",
                    "nullable": False,
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_table": {"$ref": "#/components/schemas/RefTable"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")
    model_factory(name="RefTable")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model with None ref_model
    model_instance = model(id=12, name="table name 1", ref_table=None)
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.flush()
