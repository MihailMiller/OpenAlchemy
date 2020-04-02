"""Tests for inheritance helpers."""

import types

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, exception",
    [
        ({"$ref": 1}, {}, exceptions.MalformedSchemaError),
        ({"$ref": "#/components/schemas/Parent"}, {}, exceptions.SchemaNotFoundError),
        ({"allOf": "Parent"}, {}, exceptions.MalformedSchemaError),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {},
            exceptions.SchemaNotFoundError,
        ),
        (
            {"$ref": "#/components/schemas/Other"},
            {"Other": {"$ref": "#/components/schemas/Other"}},
            exceptions.MalformedSchemaError,
        ),
        (
            {"$ref": "#/components/schemas/Other1"},
            {
                "Other1": {"$ref": "#/components/schemas/Other2"},
                "Other2": {"$ref": "#/components/schemas/Other1"},
            },
            exceptions.MalformedSchemaError,
        ),
        (
            {"$ref": "#/components/schemas/Other"},
            {"Other": {"allOf": [{"$ref": "#/components/schemas/Other"}]}},
            exceptions.MalformedSchemaError,
        ),
    ],
    ids=[
        "$ref not string",
        "$ref with parent that is not in schemas",
        "allOf not list",
        "allOf $ref with parent that is not in schemas",
        "circular $ref single step",
        "circular $ref multiple step",
        "allOf circular $ref",
    ],
)
@pytest.mark.helper
def test_check_parent_invalid(schema, schemas, exception):
    """
    GIVEN child schema and parent name, schemas and expected exception
    WHEN check_parent is called with the schema, name and schemas
    THEN the expected exception is raised.
    """
    parent_name = "Parent"

    with pytest.raises(exception):
        helpers.inheritance.check_parent(
            schema=schema, parent_name=parent_name, schemas=schemas
        )


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    [
        ({}, {}, False),
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"x-tablename": "table 1"}},
            True,
        ),
        ({"$ref": "#/components/schemas/Parent"}, {"Parent": {}}, False),
        (
            {"$ref": "#/components/schemas/Intermediate"},
            {
                "Intermediate": {"$ref": "#/components/schemas/Parent"},
                "Parent": {"x-tablename": "table 1"},
            },
            True,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate"},
            {
                "Intermediate": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Parent"},
                        {"x-inherits": False},
                    ]
                },
                "Parent": {"x-tablename": "table 1"},
            },
            False,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate"},
            {"Intermediate": {"$ref": "#/components/schemas/Parent"}, "Parent": {}},
            False,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate1"},
            {
                "Intermediate1": {"$ref": "#/components/schemas/Intermediate2"},
                "Intermediate2": {"$ref": "#/components/schemas/Parent"},
                "Parent": {"x-tablename": "table 1"},
            },
            True,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate1"},
            {
                "Intermediate1": {"$ref": "#/components/schemas/Intermediate2"},
                "Intermediate2": {"$ref": "#/components/schemas/Parent"},
                "Parent": {},
            },
            False,
        ),
        ({"allOf": []}, {}, False),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {"Parent": {"x-tablename": "table 1"}},
            True,
        ),
        ({"allOf": [{"$ref": "#/components/schemas/Parent"}]}, {"Parent": {}}, False),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent"},
                    {"$ref": "#/components/schemas/Other"},
                ]
            },
            {"Parent": {"x-tablename": "table 1"}, "Other": {}},
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Other"},
                    {"$ref": "#/components/schemas/Parent"},
                ]
            },
            {"Parent": {"x-tablename": "table 1"}, "Other": {}},
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Other1"},
                    {"$ref": "#/components/schemas/Other2"},
                ]
            },
            {"Other1": {}, "Other2": {}},
            False,
        ),
        (
            {"allOf": [{"allOf": [{"$ref": "#/components/schemas/Parent"}]}]},
            {"Parent": {"x-tablename": "table 1"}},
            True,
        ),
    ],
    ids=[
        "base empty",
        "base name match constructible",
        "base name match not constructible",
        "recursive single $ref constructable",
        "recursive single $ref constructable not inherits",
        "recursive single $ref not constructable",
        "recursive multiple $ref constructable",
        "recursive multiple $ref not constructable",
        "recursive allOf empty",
        "recursive allOf single constructible",
        "recursive allOf single not constructible",
        "recursive allOf multiple first constructible",
        "recursive allOf multiple second constructible",
        "recursive allOf multiple not constructible",
        "recursive nested allOf constructible",
    ],
)
@pytest.mark.helper
def test_check_parent(schema, schemas, expected_result):
    """
    GIVEN child schema, parent name and schemas
    WHEN check_parent is called with the child schema, parent name and schemas
    THEN the expected result is returned.
    """
    parent_name = "Parent"

    result = helpers.inheritance.check_parent(
        schema=schema, parent_name=parent_name, schemas=schemas
    )

    assert result == expected_result


@pytest.mark.parametrize(
    "schema, schemas, exception",
    [
        ({}, {}, exceptions.MalformedSchemaError),
        ({"$ref": 1}, {}, exceptions.MalformedSchemaError),
        ({"$ref": "#/components/schemas/Parent"}, {}, exceptions.SchemaNotFoundError),
        ({"allOf": "Parent"}, {}, exceptions.MalformedSchemaError),
        ({"allOf": []}, {}, exceptions.MalformedSchemaError),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {},
            exceptions.SchemaNotFoundError,
        ),
        ({"allOf": [{}]}, {}, exceptions.MalformedSchemaError),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {"Parent": {}},
            exceptions.MalformedSchemaError,
        ),
        ({"allOf": [{}, {}]}, {}, exceptions.MalformedSchemaError),
        (
            {"$ref": "#/components/schemas/Other"},
            {"Other": {"$ref": "#/components/schemas/Other"}},
            exceptions.MalformedSchemaError,
        ),
        (
            {"$ref": "#/components/schemas/Other1"},
            {
                "Other1": {"$ref": "#/components/schemas/Other2"},
                "Other2": {"$ref": "#/components/schemas/Other1"},
            },
            exceptions.MalformedSchemaError,
        ),
        (
            {"$ref": "#/components/schemas/Other"},
            {"Other": {"allOf": [{"$ref": "#/components/schemas/Other"}]}},
            exceptions.MalformedSchemaError,
        ),
    ],
    ids=[
        "empty",
        "$ref not string",
        "$ref with parent that is not in schemas",
        "allOf not list",
        "allOf empty",
        "allOf $ref with parent that is not in schemas",
        "allOf single not constructible",
        "allOf single $ref not constructible",
        "allOf multiple not constructible",
        "circular $ref single step",
        "circular $ref multiple step",
        "allOf circular $ref",
    ],
)
@pytest.mark.helper
def test_get_parent_invalid(schema, schemas, exception):
    """
    GIVEN schema, schemas and expected exception
    WHEN get_parent is called with the schema and schemas
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        helpers.inheritance.get_parent(schema=schema, schemas=schemas)


@pytest.mark.parametrize(
    "schema, schemas, expected_name",
    [
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"x-tablename": "table 1"}},
            "Parent",
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {"$ref": "#/components/schemas/Grandparent"},
                "Grandparent": {"x-tablename": "table 1"},
            },
            "Grandparent",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {"Parent": {"x-tablename": "table 1"}},
            "Parent",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {
                "Parent1": {"x-tablename": "table 1"},
                "Parent2": {"x-tablename": "table 2"},
            },
            "Parent1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {"Parent1": {"x-tablename": "table 1"}, "Parent2": {}},
            "Parent1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {"Parent1": {}, "Parent2": {"x-tablename": "table 2"}},
            "Parent2",
        ),
        (
            {"allOf": [{"allOf": [{"$ref": "#/components/schemas/Parent"}]}]},
            {"Parent": {"x-tablename": "table 1"}},
            "Parent",
        ),
    ],
    ids=[
        "$ref constructible",
        "$ref recursive constructible",
        "allOf single constructible",
        "allOf multiple constructible",
        "allOf multiple first constructible",
        "allOf multiple second constructible",
        "nested allOf",
    ],
)
@pytest.mark.helper
def test_get_parent_valid(schema, schemas, expected_name):
    """
    GIVEN schema, schemas and expected name
    WHEN get_parent is called with the schema and schemas
    THEN the expected name is returned.
    """
    name = helpers.inheritance.get_parent(schema=schema, schemas=schemas)

    assert name == expected_name


@pytest.mark.parametrize(
    "schema, schemas, exception",
    [
        ({"$ref": 1}, {}, exceptions.MalformedSchemaError),
        ({"$ref": "#/components/schemas/Parent"}, {}, exceptions.SchemaNotFoundError),
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"$ref": "#/components/schemas/Parent"}},
            exceptions.MalformedSchemaError,
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {"$ref": "#/components/schemas/Grandparent"},
                "Grandparent": {"$ref": "#/components/schemas/Parent"},
            },
            exceptions.MalformedSchemaError,
        ),
        ({"allOf": "Parent"}, {}, exceptions.MalformedSchemaError),
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"allOf": [{"$ref": "#/components/schemas/Parent"}]}},
            exceptions.MalformedSchemaError,
        ),
    ],
    ids=[
        "$ref not string",
        "$ref unresolved",
        "single step circular $ref",
        "multiple step circular $ref",
        "allOf not list",
        "allOf single step circular $ref",
    ],
)
@pytest.mark.helper
def test_get_parents_invalid(schema, schemas, exception):
    """
    GIVEN invalid schema and schemas and expected exception
    WHEN get_parents is called with the schema and schemas
    THEN the expect exception is raised.
    """
    with pytest.raises(exception):
        list(helpers.inheritance.get_parents(schema=schema, schemas=schemas))


@pytest.mark.parametrize(
    "schema, schemas, expected_parents",
    [
        ({}, {}, []),
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"x-tablename": "parent"}},
            ["Parent"],
        ),
        ({"$ref": "#/components/schemas/Parent"}, {"Parent": {}}, []),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Grandparent": {"x-tablename": "grandparent"},
            },
            ["Grandparent", "Parent"],
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {
                    "allOf": [
                        {"x-inherits": True, "x-tablename": "parent"},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Grandparent": {"x-tablename": "grandparent"},
            },
            ["Grandparent", "Parent"],
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {
                    "allOf": [
                        {"x-inherits": "Grandparent"},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Grandparent": {"x-tablename": "grandparent"},
            },
            ["Grandparent", "Parent"],
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {
                    "allOf": [
                        {"x-inherits": False, "x-tablename": "parent"},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Grandparent": {"x-tablename": "grandparent"},
            },
            ["Parent"],
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {
                "Parent": {
                    "allOf": [
                        {"x-tablename": "parent"},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Grandparent": {},
            },
            ["Parent"],
        ),
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"$ref": "#/components/schemas/Grandparent"}, "Grandparent": {}},
            [],
        ),
        ({"allOf": []}, {}, []),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {"Parent": {"x-tablename": "parent"}},
            ["Parent"],
        ),
        ({"allOf": [{"$ref": "#/components/schemas/Parent"}]}, {"Parent": {}}, []),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {
                "Parent1": {"x-tablename": "parent 1"},
                "Parent2": {"x-tablename": "parent 2"},
            },
            ["Parent1", "Parent2"],
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {"Parent1": {"x-tablename": "parent 1"}, "Parent2": {}},
            ["Parent1"],
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {"Parent1": {}, "Parent2": {"x-tablename": "parent 2"}},
            ["Parent2"],
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent1"},
                    {"$ref": "#/components/schemas/Parent2"},
                ]
            },
            {"Parent1": {}, "Parent2": {}},
            [],
        ),
    ],
    ids=[
        "empty",
        "single $ref constructable",
        "single $ref not constructable",
        "nested $ref constructable inherits bool",
        "nested $ref constructable inherits bool with tablename",
        "nested $ref constructable inherits string",
        "nested $ref constructable no inheritance",
        "nested $ref some constructable",
        "nested $ref not constructable",
        "allOf empty",
        "allOf single constructabe",
        "allOf single not constructabe",
        "allOf multiple constructabe",
        "allOf multiple first constructabe",
        "allOf multiple second constructabe",
        "allOf multiple not constructabe",
    ],
)
@pytest.mark.helper
def test_get_parents_valid(schema, schemas, expected_parents):
    """
    GIVEN schema and schemas and expected parents
    WHEN get_parents is called with the schema and schemas
    THEN the expect parents are returned.
    """
    generator = helpers.inheritance.get_parents(schema=schema, schemas=schemas)

    assert isinstance(generator, types.GeneratorType)
    assert list(generator) == expected_parents
