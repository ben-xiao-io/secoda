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

def parse_connection_string(connection_string):
    # Remove the "postgresql://" prefix
    connection_string = connection_string.replace("postgresql://", "")

    # Split the string by "@" to separate credentials and host
    credentials, host = connection_string.split("@")

    # Split the credentials by ":" to separate username and password
    username, password = credentials.split(":")

    # Split the host by ":" to separate hostname, port, and database
    host, port_database = host.split(":")
    port, db_name = port_database.split("/")

    # Return the extracted information as a dictionary
    print({
        "host": host,
        "db_name": db_name,
        "username": username,
        "password": password,
        "port": port,
    })
    return {
        "host": host,
        "db_name": db_name,
        "username": username,
        "password": password,
        "port": port,
    }


def build_metadata_json(db_info_form: DatabaseInfoForm) -> JsonResponse:
    if not db_info_form.is_valid():
        return JsonResponse({'error': db_info_form.errors})

    host = db_info_form.cleaned_data.get('host')
    db_name = db_info_form.cleaned_data.get('db_name')
    username = db_info_form.cleaned_data.get('username')
    password = db_info_form.cleaned_data.get('password')
    port = db_info_form.cleaned_data.get('port')

    conn_string = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
    print(conn_string)
    
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

@csrf_exempt
def get_table_metadata_from_str(request: HttpRequest):
    if request.method == 'POST':
        conn_str = request.POST.get("conn_str")
        if not conn_str:
            return JsonResponse({'erorr': 'Missing conn_str from body.'})

        db_info = parse_connection_string(conn_str)
        db_info_form = DatabaseInfoForm(db_info)
        # db_info_form.data['host'] = db_info['host']
        # db_info_form.data['db_name'] = db_info['db_name']
        # db_info_form.data['username'] = db_info['username']
        # db_info_form.data['password'] = db_info['password']
        # db_info_form.data['port'] = db_info['port']


        print(db_info_form.data)
        json_response = build_metadata_json(db_info_form)
        return json_response
    
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def get_table_metadata(request: HttpRequest):
    if request.method == 'POST':
        db_info_form = DatabaseInfoForm(request.POST)
        
        json_response = build_metadata_json(db_info_form)
        return json_response
    
    return JsonResponse({'error': 'Invalid request method'})


