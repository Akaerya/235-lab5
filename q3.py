import pytest

import sqlite3


def get_table_information_from_database(database_filename):
    # Bring in code from question 1
    connection = sqlite3.connect(database_filename)
    metadata_dictionary = {}
    
    with connection:
        # obtain a cursor from the connection
        cursor = connection.cursor()
        # execute the command on the cursor
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # Obtain result
        result = cursor.fetchall()


        table_names = []

        # for each row in the returned result dataset
        # add all rows to the table_names list excluding the rows that begin with "sqlite" (ie at row[0])
        # add code here:

        for row in result:
            if not "sqlite" in row[0]:
                table_names.append(row[0])

        for table_name in table_names:
            stmt = "PRAGMA table_info('{}')".format(table_name)
            cursor.execute(stmt)

            columns = cursor.fetchall()

            # for each row in the returned columns
            # populate the dictionary such that:
            # If the `table_name` is already in the dictionary, append to the existing list
            # otherwise create a new key `table_name` in the dictionary with a new list consisting of
            # the element (ie a list with element column[1]).
            for column in columns:
                if table_name in metadata_dictionary:
                    metadata_dictionary[table_name].append(column[1])
                else:
                    metadata_dictionary[table_name] = [column[1]]
    
    return metadata_dictionary


def get_best_of_albums(database_filename, column_name_for_ordering):
    metadata_dictionary = get_table_information_from_database(database_filename)

    if column_name_for_ordering not in metadata_dictionary["albums"]:
        print("ERROR: could not find column '{}' in the list of columns for table 'albums'!".format(
            column_name_for_ordering))
        return []

    # create new sqlite connection here using the `database_filename` input
    connection = sqlite3.connect(database_filename)

    result = []

    # with the context of `connection`
    with connection:

        # obtain a cursor from the connection
        cursor = connection.cursor()

        # this should be a sql command  that returns all columns
        # from albums where the title contains "Greatest Hits" OR "Best Of"
        # the returned query data should be sorted according to the input `column_name_for_ordering`.
            # hint you can choose to use .format() on the string query to insert `column_name_for_ordering`.

        stmt = "SELECT * FROM albums WHERE Title LIKE '%Greatest Hits%' OR Title Like '%Best Of%' ORDER BY {}".format(column_name_for_ordering)

        # execute the command on the cursor
        cursor.execute(stmt)

        result = cursor.fetchall()

    return result


def test_case1():
    database_filename = 'chinook.db'
    column_name_for_ordering = "ArtistId"
    query_result = get_best_of_albums(database_filename, column_name_for_ordering)

    assert query_result[1] == (20, 'The Best Of Buddy Guy - The Millenium Collection', 15)
    assert query_result[3] == (36, 'Greatest Hits II', 51)
    assert query_result[5] == (61, "Knocking at Your Back Door: The Best Of Deep Purple in the 80's", 58)
    assert query_result[7] == (83, 'My Way: The Best Of Frank Sinatra [Disc 1]', 85)


def test_case2():
    database_filename = 'chinook.db'
    column_name_for_ordering = "AlbumId"
    query_result = get_best_of_albums(database_filename, column_name_for_ordering)

    assert query_result[2] == (36, 'Greatest Hits II', 51)
    assert query_result[4] == (61, "Knocking at Your Back Door: The Best Of Deep Purple in the 80's", 58)
    assert query_result[6] == (83, 'My Way: The Best Of Frank Sinatra [Disc 1]', 85)
    assert query_result[8] == (147, 'The Best Of Men At Work', 105)

def test_case3(capfd):
    database_filename = 'chinook.db'
    column_name_for_ordering = "Id"
    query_result = get_best_of_albums(database_filename, column_name_for_ordering)
    out, err = capfd.readouterr()
    assert out == "ERROR: could not find column 'Id' in the list of columns for table 'albums'!\n"
    assert query_result == []

def test_case4():
    database_filename = 'chinook.db'
    column_name_for_ordering = "Title"
    query_result = get_best_of_albums(database_filename, column_name_for_ordering)

    assert query_result[1] == (141, 'Greatest Hits', 100)
    assert query_result[2] == (185, 'Greatest Hits I', 51)
    assert query_result[3] == (36, 'Greatest Hits II', 51)
