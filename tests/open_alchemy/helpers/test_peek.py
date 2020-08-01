"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas",
    [({}, {}), ({"type": True}, {})],
    ids=["plain", "not string value"],
)
@pytest.mark.helper
def test_type_no_type(schema, schemas):
    """
    GIVEN schema without a type
    WHEN type_ is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        helpers.peek.type_(schema=schema, schemas=schemas)


@pytest.mark.helper
def test_type():
    """
    GIVEN schema with type
    WHEN type_ is called with the schema
    THEN the type of the schema is returned.
    """
    type_ = "type 1"
    schema = {"type": type_}

    returned_type = helpers.peek.type_(schema=schema, schemas={})

    assert returned_type == type_


@pytest.mark.helper
def test_nullable_wrong_type():
    """
    GIVEN schema with nullable defined as a string
    WHEN nullable is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"nullable": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.nullable(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_nullable",
    [({}, None), ({"nullable": True}, True), ({"nullable": False}, False)],
    ids=["missing", "true", "false"],
)
@pytest.mark.helper
def test_nullable(schema, expected_nullable):
    """
    GIVEN schema and expected nullable
    WHEN nullable is called with the schema
    THEN the expected nullable is returned.
    """
    returned_nullable = helpers.peek.nullable(schema=schema, schemas={})

    assert returned_nullable == expected_nullable


@pytest.mark.helper
def test_format_wrong_type():
    """
    GIVEN schema with format defined as a boolean
    WHEN format_ is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"format": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.format_(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_format",
    [({}, None), ({"format": "format 1"}, "format 1")],
    ids=["missing", "present"],
)
@pytest.mark.helper
def test_format(schema, expected_format):
    """
    GIVEN schema and expected format
    WHEN format_ is called with the schema
    THEN the expected format is returned.
    """
    returned_format = helpers.peek.format_(schema=schema, schemas={})

    assert returned_format == expected_format


@pytest.mark.helper
def test_max_length_wrong_type():
    """
    GIVEN schema with max_length defined as a boolean
    WHEN max_length is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"maxLength": "1"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.max_length(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_max_length",
    [({}, None), ({"maxLength": 1}, 1)],
    ids=["missing", "present"],
)
@pytest.mark.helper
def test_max_length(schema, expected_max_length):
    """
    GIVEN schema and expected max_length
    WHEN max_length is called with the schema
    THEN the expected max_length is returned.
    """
    returned_max_length = helpers.peek.max_length(schema=schema, schemas={})

    assert returned_max_length == expected_max_length


@pytest.mark.helper
def test_read_only_wrong_type():
    """
    GIVEN schema with readOnly defined as a string
    WHEN read_only is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"readOnly": "true"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.read_only(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_read_only",
    [({}, None), ({"readOnly": False}, False), ({"readOnly": True}, True)],
    ids=["missing", "false", "true"],
)
@pytest.mark.helper
def test_read_only(schema, expected_read_only):
    """
    GIVEN schema and expected readOnly
    WHEN read_only is called with the schema
    THEN the expected readOnly is returned.
    """

    returned_read_only = helpers.peek.read_only(schema=schema, schemas={})

    assert returned_read_only == expected_read_only


@pytest.mark.helper
def test_write_only_wrong_type():
    """
    GIVEN schema with writeOnly defined as a string
    WHEN write_only is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"writeOnly": "true"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.write_only(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_write_only",
    [({}, None), ({"writeOnly": False}, False), ({"writeOnly": True}, True)],
    ids=["missing", "false", "true"],
)
@pytest.mark.helper
def test_write_only(schema, expected_write_only):
    """
    GIVEN schema and expected writeOnly
    WHEN write_only is called with the schema
    THEN the expected writeOnly is returned.
    """

    returned_write_only = helpers.peek.write_only(schema=schema, schemas={})

    assert returned_write_only == expected_write_only


@pytest.mark.helper
def test_description_wrong_type():
    """
    GIVEN schema with description defined as a boolean
    WHEN description is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"description": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.description(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_description",
    [({}, None), ({"description": "description 1"}, "description 1")],
    ids=["missing", "present"],
)
@pytest.mark.helper
def test_description(schema, expected_description):
    """
    GIVEN schema and expected description
    WHEN description is called with the schema
    THEN the expected description is returned.
    """
    returned_description = helpers.peek.description(schema=schema, schemas={})

    assert returned_description == expected_description


@pytest.mark.helper
def test_primary_key_wrong_type():
    """
    GIVEN schema with primary key defined as a string
    WHEN primary_key is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-primary-key": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.primary_key(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_primary_key",
    [({}, False), ({"x-primary-key": False}, False), ({"x-primary-key": True}, True)],
    ids=["missing", "false", "true"],
)
@pytest.mark.helper
def test_primary_key(schema, expected_primary_key):
    """
    GIVEN schema and expected primary key
    WHEN primary_key is called with the schema
    THEN the expected primary key is returned.
    """
    returned_primary_key = helpers.peek.primary_key(schema=schema, schemas={})

    assert returned_primary_key == expected_primary_key


@pytest.mark.helper
def test_tablename_wrong_type():
    """
    GIVEN schema with tablename defined as a boolean
    WHEN tablename is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-tablename": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.tablename(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_tablename",
    [({}, None), ({"x-tablename": "table 1"}, "table 1")],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_tablename(schema, expected_tablename):
    """
    GIVEN schema and expected tablename
    WHEN tablename is called with the schema
    THEN the expected tablename is returned.
    """
    returned_tablename = helpers.peek.tablename(schema=schema, schemas={})

    assert returned_tablename == expected_tablename


@pytest.mark.helper
def test_inherits_wrong_type():
    """
    GIVEN schema with x-inherits defined as an integer
    WHEN inherits is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-inherits": 1}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.inherits(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_inherits",
    [({}, None), ({"x-inherits": "Parent1"}, "Parent1"), ({"x-inherits": True}, True)],
    ids=["missing", "defined string", "defined boolean"],
)
@pytest.mark.helper
def test_inherits(schema, expected_inherits):
    """
    GIVEN schema and expected inherits
    WHEN inherits is called with the schema
    THEN the expected inherits is returned.
    """
    returned_inherits = helpers.peek.inherits(schema=schema, schemas={})

    assert returned_inherits == expected_inherits


@pytest.mark.helper
def test_json_wrong_type():
    """
    GIVEN schema with x-json defined as an integer
    WHEN json is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-json": 1}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.json(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_json",
    [({}, None), ({"x-json": True}, True)],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_json(schema, expected_json):
    """
    GIVEN schema and expected json
    WHEN json is called with the schema
    THEN the expected json is returned.
    """
    returned_json = helpers.peek.json(schema=schema, schemas={})

    assert returned_json == expected_json


@pytest.mark.helper
def test_backref_wrong_type():
    """
    GIVEN schema with backref defined as a boolean
    WHEN backref is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-backref": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.backref(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_backref",
    [({}, None), ({"x-backref": "table 1"}, "table 1")],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_backref(schema, expected_backref):
    """
    GIVEN schema and expected backref
    WHEN backref is called with the schema
    THEN the expected backref is returned.
    """
    returned_backref = helpers.peek.backref(schema=schema, schemas={})

    assert returned_backref == expected_backref


@pytest.mark.helper
def test_secondary_wrong_type():
    """
    GIVEN schema with secondary defined as a boolean
    WHEN secondary is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-secondary": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.secondary(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_secondary",
    [({}, None), ({"x-secondary": "table 1"}, "table 1")],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_secondary(schema, expected_secondary):
    """
    GIVEN schema and expected secondary
    WHEN secondary is called with the schema
    THEN the expected secondary is returned.
    """
    returned_secondary = helpers.peek.secondary(schema=schema, schemas={})

    assert returned_secondary == expected_secondary


@pytest.mark.helper
def test_uselist_wrong_type():
    """
    GIVEN schema with uselist defined as a boolean
    WHEN uselist is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-uselist": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.uselist(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_uselist",
    [({}, None), ({"x-uselist": True}, True)],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_uselist(schema, expected_uselist):
    """
    GIVEN schema and expected uselist
    WHEN uselist is called with the schema
    THEN the expected uselist is returned.
    """
    returned_uselist = helpers.peek.uselist(schema=schema, schemas={})

    assert returned_uselist == expected_uselist


@pytest.mark.helper
def test_items_wrong_type():
    """
    GIVEN schema with items defined as a boolean
    WHEN items is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"items": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.items(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_items",
    [({}, None), ({"items": {"key": "value"}}, {"key": "value"})],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_items(schema, expected_items):
    """
    GIVEN schema and expected items
    WHEN items is called with the schema
    THEN the expected items is returned.
    """
    returned_items = helpers.peek.items(schema=schema, schemas={})

    assert returned_items == expected_items


@pytest.mark.helper
def test_kwargs_wrong_type():
    """
    GIVEN schema with kwargs defined as a boolean
    WHEN kwargs is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-kwargs": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.kwargs(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_kwargs",
    [({}, None), ({"x-kwargs": {"key": "value"}}, {"key": "value"})],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_kwargs(schema, expected_kwargs):
    """
    GIVEN schema and expected kwargs
    WHEN kwargs is called with the schema
    THEN the expected kwargs is returned.
    """
    returned_kwargs = helpers.peek.kwargs(schema=schema, schemas={})

    assert returned_kwargs == expected_kwargs


@pytest.mark.helper
def test_ref_wrong_type():
    """
    GIVEN schema with $ref defined as a boolean
    WHEN $ref is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"$ref": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.ref(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_ref",
    [
        ({}, None),
        ({"$ref": "value"}, "value"),
        ({"allOf": [{"$ref": "value"}]}, "value"),
    ],
    ids=["missing", "defined", "allOf"],
)
@pytest.mark.helper
def test_ref(schema, expected_ref):
    """
    GIVEN schema and expected $ref
    WHEN $ref is called with the schema
    THEN the expected $ref is returned.
    """
    returned_ref = helpers.peek.ref(schema=schema, schemas={})

    assert returned_ref == expected_ref


@pytest.mark.helper
def test_foreign_key_column_wrong_type():
    """
    GIVEN schema with foreign-key-column defined as a boolean
    WHEN foreign_key_column is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-foreign-key-column": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.foreign_key_column(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_foreign_key_column",
    [({}, None), ({"x-foreign-key-column": "id"}, "id")],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_foreign_key_column(schema, expected_foreign_key_column):
    """
    GIVEN schema and expected foreign-key-column
    WHEN foreign_key_column is called with the schema
    THEN the expected foreign_key_column is returned.
    """
    returned_foreign_key_column = helpers.peek.foreign_key_column(
        schema=schema, schemas={}
    )

    assert returned_foreign_key_column == expected_foreign_key_column


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "integer", "default": "1"},
        {"type": "string", "maxLength": 1, "default": "value 1"},
    ],
    ids=["default different to schema type", "default different to schema maxLength"],
)
@pytest.mark.helper
def test_default_invalid(schema):
    """
    GIVEN schema with an invalid default
    WHEN default is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.default(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, schemas, expected_default",
    [
        ({"type": "integer"}, {}, None),
        ({"type": "integer", "default": 1}, {}, 1),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "integer", "default": 1}},
            1,
        ),
        ({"type": "integer", "format": "int32", "default": 1}, {}, 1),
    ],
    ids=["no default", "default given", "$ref with default", "format with default"],
)
@pytest.mark.helper
def test_default(schema, schemas, expected_default):
    """
    GIVEN schema
    WHEN default is called with the schema
    THEN the expected default value is returned.
    """
    default = helpers.peek.default(schema=schema, schemas=schemas)

    assert default == expected_default


@pytest.mark.parametrize(
    "schema, schemas, expected_value",
    [
        ({}, {}, None),
        ({"key": "value 1"}, {}, "value 1"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value 1"}},
            "value 1",
        ),
        ({"allOf": []}, {}, None),
        ({"allOf": [{"key": "value 1"}]}, {}, "value 1"),
        ({"allOf": [{}]}, {}, None),
        ({"allOf": [{"key": "value 1"}, {"key": "value 2"}]}, {}, "value 1"),
        ({"allOf": [{"key": "value 2"}, {"key": "value 1"}]}, {}, "value 2"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value 1"}]}},
            "value 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value 1"}]}},
            "value 1",
        ),
    ],
    ids=[
        "missing",
        "plain",
        "$ref",
        "allOf empty",
        "allOf single no type",
        "allOf single",
        "allOf multiple first",
        "allOf multiple last",
        "$ref then allOf",
        "allOf with $ref",
    ],
)
@pytest.mark.helper
def test_peek_key(schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN peek_key is called with the schema and schemas
    THEN the expected value is returned.
    """
    returned_type = helpers.peek.peek_key(schema=schema, schemas=schemas, key="key")

    assert returned_type == expected_value


@pytest.mark.parametrize(
    "schema, schemas",
    [
        pytest.param({"$ref": True}, {}, id="$ref not string"),
        pytest.param({"allOf": True}, {}, id="allOf list"),
        pytest.param({"allOf": [True]}, {}, id="allOf element not dict"),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"$ref": "#/components/schemas/RefSchema"}},
            id="single step circular $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {"$ref": "#/components/schemas/NestedRefSchema"},
                "NestedRefSchema": {"$ref": "#/components/schemas/RefSchema"},
            },
            id="multiple step circular $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}},
            id="allOf single step circular $ref",
        ),
    ],
)
@pytest.mark.helper
def test_peek_key_invalid(schema, schemas):
    """
    GIVEN schema, schemas that are invalid
    WHEN peek_key is called with the schema and schemas
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.peek_key(schema=schema, schemas=schemas, key="key")
