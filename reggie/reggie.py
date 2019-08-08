# -*- coding: utf-8 -*-

"""Main module."""
from typing import List, TextIO
import re


def collect_created_tables(text_stream: TextIO) -> List[str]:
    tables = []
    pattern = r'(?:table|view)\s+(\w+\.?\w*)'
    return re.findall(pattern, text_stream.read(), re.IGNORECASE | re.MULTILINE)
