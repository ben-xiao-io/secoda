from django.db import models

from typing import List

class ColumnMetadata:
    def __init__(self, col_name: str, col_type: str):
        self.col_name = col_name
        self.col_type = col_type

    def __iter__(self):
        yield 'col_name', self.col_name
        yield 'col_type', self.col_type

class TableMetadata:
    def __init__(self, schema: str, columns: List[ColumnMetadata], num_rows: int, database: str):
        self.schema = schema
        self.columns = columns
        self.num_rows = num_rows
        self.database = database

    def __iter__(self):
        yield 'columns', [ dict(col) for col in self.columns ]
        yield 'num_rows', self.num_rows
        yield 'schema', self.schema
        yield 'database', self.database
