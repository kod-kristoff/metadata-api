"""Tests for parse_yaml module."""

import logging
from collections import defaultdict
from pathlib import Path

from metadata_api.parse_yaml import _get_schema, _process_yaml_file  # noqa: PLC2701

YAML_CONTENT: str = """
name:
    swe: temp
license: MIT license
type: utility
"""


def test__process_yaml_file_fails_with_bad_instance(caplog) -> None:  # noqa: ANN001, D103
    filepath = Path("tests/assets/gen/tempfile.yaml")
    filepath.write_text(YAML_CONTENT, encoding="utf-8")
    resource_texts = defaultdict(dict)
    resource_schema = _get_schema(Path("tests/assets/schema/metadata.json"))
    assert resource_schema is not None
    collection_mappings = {}
    localizations = {}
    license_info = {}
    with caplog.at_level(logging.INFO):
        _process_yaml_file(
            filepath, resource_texts, collection_mappings, resource_schema, localizations, license_info, offline=True
        )

    print(caplog.text)
    assert '"MIT license" is not one of' in caplog.text
