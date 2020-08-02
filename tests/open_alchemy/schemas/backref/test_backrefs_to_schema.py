"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref

BackArt = backref._BackrefArtifacts  # pylint: disable=protected-access


class TestBackrefsToSchema:
    """Tests for _backrefs_to_schema"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "backrefs, expected_schema",
        [
            pytest.param([], {"type": "object", "x-backrefs": {}}, id="empty"),
            pytest.param(
                [BackArt("Schema1", "prop_1", {"key_1": "value 1"})],
                {"type": "object", "x-backrefs": {"prop_1": {"key_1": "value 1"}}},
                id="single",
            ),
            pytest.param(
                [
                    BackArt("Schema1", "prop_1", {"key_1": "value 1"}),
                    BackArt("Schema1", "prop_2", {"key_2": "value 2"}),
                ],
                {
                    "type": "object",
                    "x-backrefs": {
                        "prop_1": {"key_1": "value 1"},
                        "prop_2": {"key_2": "value 2"},
                    },
                },
                id="multiple",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(backrefs, expected_schema):
        """
        GIVEN backrefs and expected schema
        WHEN _backrefs_to_schema is called with the backrefs
        THEN the expected schema is returned.
        """
        returned_schema = backref._backrefs_to_schema(backrefs)

        assert returned_schema == expected_schema
