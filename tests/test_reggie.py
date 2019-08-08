#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `reggie` package."""
from io import StringIO
import re

import pytest

from reggie.reggie import (
    collect_created_tables,
    get_table_names_from_script,
    get_matches_in_directory,
    FileMatch,
    get_matches_in_script,
    Table,
)


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
        assert [Table(name='kittens', obj_type='table')] == collect_created_tables(
            single_table_str
        )

    def test_it_parses_simple_table_statements_witout_case_sensitivity(
        self, single_table_str_caps
    ):
        assert [Table(name='kittens', obj_type='table')] == collect_created_tables(
            single_table_str_caps
        )

    def test_it_parses_simple_view_statements(self, single_view_str_caps):
        assert [Table(name='kittens', obj_type='view')] == collect_created_tables(
            single_view_str_caps
        )

    def test_it_parses_view_split_across_lines(self, view_str_split_across_lines):
        assert [Table(name='kittens', obj_type='view')] == collect_created_tables(
            view_str_split_across_lines
        )

    def test_it_parses_schema_and_table_names(self, view_schema_and_table):
        assert [Table(name='fuzzy.bunnies', obj_type='view')] == collect_created_tables(
            view_schema_and_table
        )

    def test_it_parses_multiple_table_statements(self, multiple_table_str):
        assert [
            Table(name='fuzzy.bunnies', obj_type='table'),
            Table(name='kittens', obj_type='view'),
        ] == collect_created_tables(multiple_table_str)


class TestGetTableNamesFromScript:
    def test_it_returns_tables_from_script(self):
        path = 'tests/fixtures/simple-script.sql'
        assert [
            Table(name='fuzzy.bunnies', obj_type='table'),
            Table(name='kittens', obj_type='view'),
        ] == get_table_names_from_script(path)

    def test_it_returns_no_tables_from_empty_script(self):
        path = 'tests/fixtures/empty.sql'
        assert [] == get_table_names_from_script(path)


class TestGetMatchesInScript:
    def test_it(self):
        file_name = 'tests/fixtures/small_animals/bunnies/american/bugs.sql'

        regex = re.compile(f'kittens')
        expected = [
            FileMatch(
                table='kittens',
                path='tests/fixtures/small_animals/bunnies/american/bugs.sql',
            )
        ]
        assert expected == get_matches_in_script(file_name, regex)


class TestGetMatchesInDirectory:
    def test_it(self):
        path = 'tests/fixtures/small_animals'
        tables = ['fuzzy.bunnies', 'kittens']
        expected = [
            FileMatch(
                table='kittens',
                path='tests/fixtures/small_animals/bunnies/american/bugs.sql',
            ),
            FileMatch(
                table='fuzzy.bunnies',
                path='tests/fixtures/small_animals/bunnies/american/bugs.sql',
            ),
            FileMatch(
                table='kittens',
                path='tests/fixtures/small_animals/teacup_pigs/porky.sql',
            ),
        ]
        assert set(expected) == set(get_matches_in_directory(tables, path))
