import pytest

import sqlite3


def perform_query_for_whole_table(database_filename, table_name):
    result = []

    connection = sqlite3.connect(database_filename)

    with connection:

        # obtain a cursor from the connection
        cursor = connection.cursor()
        # cursor = ...

        stmt = f"SELECT * FROM {table_name}"

        # execute the command on the cursor
        cursor.execute(stmt)
        # cursor.execute( ...

        # Obtain result
        result = cursor.fetchall()
        # complete the code:
        #result = ()

    return result

def test_case1():
    database_filename = 'chinook.db'
    table_name = 'artists'

    query_result = perform_query_for_whole_table(database_filename, table_name)

    assert query_result[0] == (1, 'AC/DC')
    assert query_result[3] == (4, 'Alanis Morissette')

    #for database_record in query_result[0:20]:
    #    print(database_record)

def test_case2():
    database_filename = 'chinook.db'
    table_name = 'genres'

    query_result = perform_query_for_whole_table(database_filename, table_name)

    assert query_result[9] == (10, 'Soundtrack')
