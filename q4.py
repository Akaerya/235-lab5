import pytest

import sqlite3


def get_best_of_albums_include_artists(database_filename):

    # create sqlite connection here using the `database_filename` input
    connection = sqlite3.connect(database_filename)

    # obtain a cursor from the connection
    cursor = connection.cursor()

    # this should be a sql that returns all album ids, titles and artist names
    # from albums where the title contains "Greatest Hits" OR "Best Of"
    # the returned query data should be sorted according to the artists name.
    #
    # hint use an inner join to match albums to artists to get all necessary return types
    stmt = "SELECT AL.AlbumId, AL.Title,AR.name \
    FROM albums AL JOIN artists AR ON AL.ArtistId = AR.ArtistId \
    WHERE AL.Title LIKE '%Greatest Hits%' OR AL.Title \
    LIKE '%Best Of%' ORDER BY AR.Name"


    # execute the command on the cursor
    cursor.execute(stmt)

    # Obtain result
    result = cursor.fetchall()

    # Then close connection
    connection.close()
    
    return result


def test_case1():
    database_filename = 'chinook.db'
    query_result = get_best_of_albums_include_artists(database_filename)

    assert len(query_result)==21
    assert query_result[0] == (13, 'The Best Of Billy Cobham', 'Billy Cobham')
    assert query_result[10] == (36, 'Greatest Hits II', 'Queen')
    assert query_result[20] == (243, 'The Best Of Van Halen, Vol. I', 'Van Halen')
