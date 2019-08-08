#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `reggie` package."""
from io import StringIO

import pytest

from reggie.reggie import collect_created_tables


@pytest.fixture
def single_table_str() -> StringIO:
    return StringIO(
        """\
    CREATE table kittens AS SELECT * FROM raw.kittens;
"""
    )


@pytest.fixture
def single_table_str_caps() -> StringIO:
    return StringIO(
        """\
    CREATE TABLE kittens AS SELECT * FROM raw.kittens;
"""
    )


@pytest.fixture
def single_view_str_caps() -> StringIO:
    return StringIO(
        """\
    CREATE VIEW kittens AS SELECT * FROM raw.kittens;

"""
    )


@pytest.fixture
def view_str_split_across_lines() -> StringIO:
    return StringIO(
        """\
    CREATE VIEW 

   kittens AS SELECT * FROM raw.kittens;

"""
    )


@pytest.fixture
def view_schema_and_table() -> StringIO:
    return StringIO(
        """\
    CREATE VIEW fuzzy.bunnies AS SELECT * FROM raw.bunnies;
"""
    )


@pytest.fixture
def multiple_table_str() -> StringIO:
    return StringIO(
        """\
    CREATE Table fuzzy.bunnies AS SELECT * FROM raw.bunnies;

    CREATE VIEW kittens AS SELECT * FROM raw.bunnies;
"""
    )


class TestCollectCreatedTables:
    def test_it_parses_simple_table_statements(self, single_table_str):
        assert ['kittens'] == collect_created_tables(single_table_str)

    def test_it_parses_simple_table_statements_witout_case_sensitivity(
        self, single_table_str_caps
    ):
        assert ['kittens'] == collect_created_tables(single_table_str_caps)

    def test_it_parses_simple_view_statements(self, single_view_str_caps):
        assert ['kittens'] == collect_created_tables(single_view_str_caps)

    def test_it_parses_view_split_across_lines(self, view_str_split_across_lines):
        assert ['kittens'] == collect_created_tables(view_str_split_across_lines)

    def test_it_parses_schema_and_table_names(self, view_schema_and_table):
        assert ['fuzzy.bunnies'] == collect_created_tables(view_schema_and_table)

    def test_it_parses_multiple_table_statements(self, multiple_table_str):
        assert ['fuzzy.bunnies', 'kittens'] == collect_created_tables(
            multiple_table_str
        )
