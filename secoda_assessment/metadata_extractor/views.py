from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from sqlalchemy import create_engine, inspect, text, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.engine import Engine
from sqlalchemy.sql.schema import Table, Column

from .models import TableMetadata, ColumnMetadata
from .forms import DatabaseInfoForm

from typing import List

@csrf_exempt
def get_table_metadata(request: HttpRequest):
    if request.method == 'POST':
        db_info_form = DatabaseInfoForm(request.POST)
        if not db_info_form.is_valid():
            return JsonResponse({'error': db_info_form.errors})

        host = db_info_form.cleaned_data.get('host')
        db_name = db_info_form.cleaned_data.get('db_name')
        username = db_info_form.cleaned_data.get('username')
        password = db_info_form.cleaned_data.get('password')
        port = db_info_form.cleaned_data.get('port')

        conn_string = f"postgresql://{username}:{password}@{host}:{port}"
        
        try:
            engine = create_engine(conn_string)
            connection = engine.connect()
            metadata = MetaData()
            metadata.reflect(bind = engine)
            tables = metadata.sorted_tables

            table_metadata_list = []
            for table in tables:
                columns = []
                for column in table.columns:
                    column_metadata = ColumnMetadata(column.name, str(column.type))
                    columns.append(column_metadata)

                table_metadata = TableMetadata(
                    columns=columns,
                    num_rows=connection.execute(text(f'SELECT COUNT(*) FROM {table.name}')).scalar(),

                    # unsure why table.schema returns None
                    # but sqlalchemy.sql.schema.Table line 822 suggest the schema
                    # doesn't exist in the metadata since all cases are handled
                    schema=table.schema,

                    # the database name is the same for all tables 
                    # because of constant conn_string
                    database=db_name,
                )
                table_metadata_list.append(table_metadata)

            return JsonResponse({'data': list(map(lambda metadata: dict(metadata), table_metadata_list))})

        except SQLAlchemyError as err:
            return JsonResponse({'error': str(err)})
    
    return JsonResponse({'error': 'Invalid request method'})
