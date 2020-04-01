"""Helpers to support inheritance."""

from .. import exceptions
from .. import types
from . import ref as ref_helper
from . import schema as schema_helper


def check_parent(
    *, schema: types.Schema, parent_name: str, schemas: types.Schemas
) -> bool:
    """
    Check that the parent is in the inheritance chain of a schema.

    Recursive function. The base cases are:
    1. the schema has $ref where the name matches the parent name if
        a. the referenced schema is constructable, return True or
        b. if the referenced schema is not constructable, return False and
    2. the schema does not have $ref nor allOf in which case return False.

    The recursive cases are:
    1. the schema has $ref where the name does not match the parent name in which case
        the function is called with the referenced schema and
    2. the schema has allOf where the function is called on each element in allOf and,
        if True is returned for any of them, True is returned otherwise False is
        returned.

    Raise MalformedSchemaError if the parent is not found in the chain.
    Raise MalformedSchemaError if the parent does not have x-tablename nor x-inherits.

    Args:
        schema: The schema to check.
        parent_name: The parent to check for in the inheritance chain.
        schemas: All the schemas.

    Returns:
        Whether the parent is in the inheritance chain.

    """
    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        return False

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check for name match base case
        if ref_name == parent_name:
            return schema_helper.constructable(schema=ref_schema, schemas=schemas)

        # Recursive case
        return check_parent(schema=ref_schema, parent_name=parent_name, schemas=schemas)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    return any(
        check_parent(schema=sub_schema, parent_name=parent_name, schemas=schemas)
        for sub_schema in all_of
    )


def get_parent(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the name of the parent of the schema.

    Recursive function. The base cases are:
    1. the schema has $ref and the referenced schema is constructable.

    The recursive cases are:
    1. the schema has $ref where the referenced schema is not constructable in which
        case the function is called with the referenced schema and
    2. the schema has allOf in which case the return value of the first element that
        does not raise the MalformedSchemaError is returned.

    Raise MalformedSchemaError if the schema does not have $ref nor allOf.
    Raise MalformedSchemaError if the schema has allOf and all of the elements raise
        MalformedSchemaError.

    Check for an immediate $ref
    """
    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is marked as inhereting does not reference a valid parent."
        )

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check whether the referenced schema is constructible
        if schema_helper.constructable(schema=ref_schema, schemas=schemas):
            return ref_name

        # Recursive case
        return get_parent(schema=ref_schema, schemas=schemas)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    # Find first constructable schema
    for sub_schema in all_of:
        try:
            return get_parent(schema=sub_schema, schemas=schemas)
        except exceptions.MalformedSchemaError:
            pass
    # None of the schemas in allOf are constructable
    raise exceptions.MalformedSchemaError(
        "A schema that is marked as inhereting does not reference a valid parent."
    )
