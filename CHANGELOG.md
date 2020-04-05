# Release Notes

## Version _next_

- Add section of documentation for each example.
- Add support for keyword arguments for relationships used to define relationship arguments not specifically handled by an extension property.
- Add support for kwargs at the model, column and foreign key level.
- Add support for single and joined table inheritance.

## Version 1.0.0 - 2020-03-21

- Add support for remote references to a file at a URL.
- Add support for default values.
- Add check for whether the value of an extension property is null.

## Version 0.14.0 - 2020-02-21

- Add support for remote references to another file on the file system.

## Version 0.13.0 - 2020-02-16

- Ring fence SQLAlchemy dependency to a facade and integration tests.
- Add tests for examples.
- Add _from_str_ and _to_str_ to complement _from_dict_ and _to_dict_ for de-serializing and serializing from JSON.
- Ring fence jsonschema dependency into a facade.
- Add description from OpenAPI specification into the models file.

## Version 0.12.1 - 2020-01-12

- Fix bug where auto generating models file meant that multiple classes with the same name were registered with the base.

## Version 0.12.0 - 2020-01-04

- Fix bug where format and maxLength was not considered for the foreign key constructed for an object reference.
- Refactor object reference handling to be easier to understand.
- Add checking whether the column is automatically generated to determining the type of a column.
- Remove typing_extensions dependency for Python version 3.8 and later.
- Add support for _nullable_ for object references.
- Add type hints for _\_\_init\_\__ and _from_dict_.
- Add example for alembic interoperability.

## Version 0.11.0 - 2019-12-29

- Add support for _password_
- Add support for _binary_
- Add support for _byte_
- Add support for _date_
- Move SQLAlchemy relationship construction behind facade
- Move schema calculations into separate files
- Refactor handling array references to reduce scope of individual tests and make them easier to understand
- Add optional parameter that can be used to generate a models file for IDE auto complete and type hinting
- Add _from_dict_ and _to_dict_ to the type models file
- Add SQLAlchemy information to models file
- Add back references to models file

## Version 0.10.4 - 2019-12-18

- Fix bug where some static files where not included in the distribution.

## Version 0.10.1 - 2019-12-15

- Refactor column handler to first check the schema, then gather the required artifacts for column construction and then construct the column.
- Add support for DateTime.

## Version 0.10.0 - 2019-11-23
_Beta release_

- Add check for whether foreign key for relationship is already constructed before automatically constructing it.
- Add support for returning parent properties in the child _to_dict_ call using _readOnly_ properties.
- Add support for many to many relationships.

## Version 0.9.1 - 2019-11-11

- Fix bug where some static files where not included in the distribution.

## Version 0.9.0 - 2019-11-10

- Add _from_dict_ and _to_dict_ functions to all models that are used to construct a model from a dictionary and to convert a model instance to a dictionary, respectively.
- Add _x-foreign-key-column_ extension property to define a custom foreign key constraint for many to one relationships.
- Add _x-composite-unique_ extension property at the object level to construct unique constraints with multiple columns.
- Add _x-composite-index_ extension property at the object level to construct indexes with multiple columns.
- Add support for one to one relationships.
- Fix bug where _allOf_ merging would only return the properties of the last object instead of merging the properties.
- Add support for one to many relationships.

## Version 0.8.0 - 2019-11-03
- Add less verbose initialisation with _init_yaml_ and _init_json_.
- Remove need for separate models file by exposing _Base_ and constructed models at _open_alchemy.models_.
- Update name from OpenAPI-SQLAlchemy to OpenAlchemy

## Version 0.7.0 - 2019-10-27
- Add support for Python 3.6.
- Add connexion example application.
- Fixed bug where referencing a schema which uses allOf in many to one relationships does not merge the allOf statement.
- Fixed bug where a type hint that is not always exported from SQLAlchemy may cause an no member error.
- Add schema checking for extension properties.

## Version 0.6.3 - 2019-10-19
- Add support for backref for many to one relationships.
- Refactor to remove reference resolving decorator.
- Add integration tests for major features.

## Version 0.6.2 - 2019-10-19
- Add support for python 3.8.

## Version 0.6.1 - 2019-10-19
- Update name from openapi-SQLAlchemy to OpenAPI-SQLAlchemy. All urls are expected to keep working.

## Version 0.6.0 - 2019-10-6
- Add support for _allOf_ for models.

## Version 0.5.0 - 2019-09-29
- Refactor column factory to use fewer decorators.
- Change exceptions to include the schema name.
- Add support for _$ref_ for models.

## Version 0.4.0 - 2019-09-21
- Add support for _allOf_ for columns.

## Version 0.3.0 - 2019-09-08
- Add support for _autoincrement_.
- Add support for _$ref_ for columns referencing other table objects.
- Add documentation

## Version 0.2.0 - 2019-08-25
- Add support for _$ref_ for columns.

## Version 0.1.1 - 2019-08-18
- Move typing-extensions development to package dependency.

## Version 0.1.0 - 2019-08-18
- Initial release
- Add support for _integer_ columns.
- Add support for _boolean_ columns.
- Add support for _number_ columns.
- Add support for _string_ columns.
