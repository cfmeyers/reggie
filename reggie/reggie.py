# -*- coding: utf-8 -*-

"""Main module."""
from typing import List, TextIO, NamedTuple, Pattern
from itertools import groupby
import re
from pathlib import Path


class FileMatch(NamedTuple):
    table: str
    path: str


class ConsolidatedFileMatch(NamedTuple):
    tables: List[str]
    path: str


def collect_created_tables(text_stream: TextIO) -> List[str]:
    pattern = r'(?:table|view)(?! if)\s+(\w+\.?\w*)'
    text = text_stream.read()
    return re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)


def get_table_names_from_script(script_path: str) -> List[str]:
    with open(script_path, 'r') as f:
        return collect_created_tables(f)


def get_matches_in_script(script_path: str, regex: Pattern) -> List[FileMatch]:
    matches = []
    with open(script_path, 'r') as f:
        for table in regex.findall(f.read()):
            matches.append(FileMatch(table=table, path=script_path))
    return matches


def get_matches_in_directory(tables: List[str], dir_path: str) -> List[FileMatch]:
    matches = []
    regex = re.compile('|'.join(tables))
    for file_path in Path(dir_path).glob('**/*.sql'):
        script_matches = get_matches_in_script(str(file_path), regex)
        matches.extend(script_matches)
    return matches


def get_consolidated_matches(matches: List[FileMatch]) -> List[ConsolidatedFileMatch]:
    matches.sort(key=lambda x: x.path)
    consolidated = []
    for k, g in groupby(matches, lambda x: x.path):
        tables = list(set([m.table for m in g]))
        cfm = ConsolidatedFileMatch(path=k, tables=tables)
        consolidated.append(cfm)
    return consolidated


def render(tables: List[str], matches: List[FileMatch]):
    consolidated_matches = get_consolidated_matches(matches)
    print('Table/View DDLs found:')
    for table in set(tables):
        print(f'\t{table}')
    print()
    for match in consolidated_matches:
        print(match.path)
        print('\t' + '\n\t'.join(match.tables))
        print('---')
        print()


def sniff_out_dependencies(target_script_path: str, dir_path: str):
    tables = get_table_names_from_script(target_script_path)
    if tables == []:
        print(f'No table or view DDLs found in {target_script_path}')
        return
    matches = get_matches_in_directory(tables, dir_path)
    render(tables, matches)
