import pytest

import sqlite3


def get_all_artists_with_at_least_n_albums(database_filename, n):
    # create sqlite connection here using the `database_filename` input
    connection = sqlite3.connect(database_filename)

    # obtain a cursor from the connection
    cursor = connection.cursor()

    # this should be a sql that returns all artist ids, artist names, and the Number of albums
    # The returned tuples should only include artists with greater than or equal to `n` parameter
    # album count.
    # The returned dataset should be ordered by the number of albums descending, and if the number is the same, then
    # by the artists name ascending.

    # The returned dataset should not have multiple tuples for the same artist
    # - the count of albums should be together in 1 tuple representing the artist.
    # - Hint: use `GROUP BY`

    # Hint: use an inner join to match artists to albums to get all necessary return types
    stmt = "SELECT AR.ArtistId AS 'Artist ID', AR.name AS 'Artist name', count(AL.AlbumId) AS 'Number of albums'\
            FROM albums AL JOIN artists AR ON AL.ArtistId = AR.ArtistId\
            GROUP BY AR.name\
            HAVING count(AL.AlbumId) >= " + str(n) + "\
            ORDER BY count(AL.AlbumId) DESC, AR.name ASC"

    # execute the command on the cursor
    cursor.execute(stmt)

    # Obtain result
    result = cursor.fetchall()
    # Then close connection
    connection.close()

    return result


def test_case1():
    database_filename = 'chinook.db'
    n = 4
    query_result = get_all_artists_with_at_least_n_albums(database_filename, n)
    assert len(query_result) ==12
    print("(artist id, artist name, number of albums):")
    assert query_result[11] == (21, 'Various Artists', 4)


def test_case2():
    database_filename = 'chinook.db'
    n = 8
    query_result = get_all_artists_with_at_least_n_albums(database_filename, n)
    assert len(query_result) == 5
    assert query_result[4] == (150, 'U2', 10)

        
def test_case3():
    database_filename = 'chinook.db'
    n = 2
    query_result = get_all_artists_with_at_least_n_albums(database_filename, n)
    assert len(query_result) == 56
    assert query_result[55] == (146, 'Titas', 2)
