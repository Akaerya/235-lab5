import pytest

import sqlite3


def get_table_information_from_database(database_filename):
    # create sqlite connection here using the `database_filename` input
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


# Test case for question one
def test_case1():
    database_filename = 'chinook.db'
    metadata_dictionary = get_table_information_from_database(database_filename)

    tables = []
    for table in sorted(metadata_dictionary.keys()):
        tables.append(table)

    assert tables == ['albums', 'artists', 'customers', 'employees', 'genres', 'invoice_items', 'invoices', 'media_types', 'playlist_track', 'playlists', 'tracks']

    assert metadata_dictionary['albums'] == ['AlbumId', 'Title', 'ArtistId']
    assert metadata_dictionary['artists'] == ['ArtistId', 'Name']
    assert metadata_dictionary['customers'] == ['CustomerId', 'FirstName', 'LastName', 'Company', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email', 'SupportRepId']
    assert metadata_dictionary['employees'] == ['EmployeeId', 'LastName', 'FirstName', 'Title', 'ReportsTo', 'BirthDate', 'HireDate', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email']
    assert metadata_dictionary['genres'] == ['GenreId', 'Name']
    assert metadata_dictionary['invoice_items'] == ['InvoiceLineId', 'InvoiceId', 'TrackId', 'UnitPrice', 'Quantity']
    assert metadata_dictionary['invoices'] == ['InvoiceId', 'CustomerId', 'InvoiceDate', 'BillingAddress', 'BillingCity', 'BillingState', 'BillingCountry', 'BillingPostalCode', 'Total']
    assert metadata_dictionary['media_types'] == ['MediaTypeId', 'Name']
    assert metadata_dictionary['playlist_track'] == ['PlaylistId', 'TrackId']
    assert metadata_dictionary['playlists'] == ['PlaylistId', 'Name']
    assert metadata_dictionary['tracks'] == ['TrackId', 'Name', 'AlbumId', 'MediaTypeId', 'GenreId', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice']


