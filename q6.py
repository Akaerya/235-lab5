import sqlite3


def get_playlist(database_filename, which_playlist):
    # create sqlite connection here using the `database_filename` input
    connection = sqlite3.connect(database_filename)

    # obtain a cursor from the connection
    cursor = connection.cursor()

    # this should be a sql that returns all PlaylistIds and Names,
    # from the playlists table if the Name is equal to `which_playlist`
    #
    stmt = "SELECT PlaylistId, Name FROM playlists WHERE Name='" + which_playlist + "'"

    # execute the command on the cursor
    cursor.execute(stmt)

    # Obtain result
    result = cursor.fetchall()

    # Using the result check that at least 1 result is returned
    # if not print an error and return an empty list.
    # add code here

    if len(result) == 0:
        print("ERROR: Could not find playlist '{}' in database!".format(which_playlist))
        return []

    playlist_id = result[0][0]
    # print(playlist_id)

    # sql_stmt is a sql query that returns all track names, album titles, genre names, artist names,and track composers,
    # for tracks that are on the playlist indicated by `which_playlist`. (use `playlist_id` defined above)
    #
    # Hint: think about which tables need to be joined and on what columns they should be joined on.
    #       - especially which column that playlist_track should be joined on.

    # hint: the query should make use of the `playlist_id` parameter.
    sql_stmt = "SELECT tracks.Name, album.Title, genre.Name, artist.Name, tracks.Composer FROM tracks \
                INNER JOIN albums album ON tracks.AlbumId=album.AlbumId \
                INNER JOIN genres genre ON tracks.GenreId=genre.GenreId \
                INNER JOIN artists artist ON album.ArtistId=artist.ArtistId \
                INNER JOIN playlist_track pt ON pt.PlaylistId = {} \
                WHERE tracks.TrackId = pt.TrackId ".format(playlist_id)

    # execute the `sql_stmt` command on the cursor
    cursor.execute(sql_stmt)

    # Obtain result
    result = cursor.fetchall()

    # Then close connection
    connection.close()

    return result


def test_case1():
    database_filename = 'chinook.db'
    which_playlist = 'On-The-Go 1'
    query_result = get_playlist(database_filename, which_playlist)

    print(f"Playlist '{which_playlist}'")
    for count, database_record in enumerate(query_result):
        print(f"{count:<2} Track Name: {database_record[0]}")
        assert database_record[0] == "Now's The Time"
        print(f"   Album Title: {database_record[1]}")
        assert database_record[1] == "The Essential Miles Davis [Disc 1]"
        print(f"   Genre: {database_record[2]}")
        assert database_record[2] == "Jazz"
        print(f"   Artist: {database_record[3]}")
        assert database_record[3] == "Miles Davis"
        print(f"   Composer: {database_record[3]}")


def test_case2():
    database_filename = 'chinook.db'
    which_playlist = 'Heavy Metal Classic'
    query_result = get_playlist(database_filename, which_playlist)

    print(f"Playlist '{which_playlist}'")
    assert len(query_result) == 26
    assert (query_result[3]) == ('Restless and Wild', 'Restless and Wild', 'Rock', 'Accept', 'F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman')
    for count, database_record in enumerate(query_result):
        print(f"{count:<2} Track Name: {database_record[0]}")
        print(f"   Album Title: {database_record[1]}")
        print(f"   Genre: {database_record[2]}")
        print(f"   Artist: {database_record[3]}")
        print(f"   Composer: {database_record[4]}")


def test_case3(capfd):

    database_filename = 'chinook.db'
    which_playlist = 'Independent'
    query_result = get_playlist(database_filename, which_playlist)
    out, err = capfd.readouterr()
    assert out == "ERROR: Could not find playlist 'Independent' in database!\n"
    assert query_result == []


def test_case4():
    database_filename = 'chinook.db'
    which_playlist = 'Grunge'
    query_result = get_playlist(database_filename, which_playlist)
    assert len(query_result) == 15
    assert query_result[6] == ('On A Plain', 'Nevermind', 'Rock', 'Nirvana', 'Kurt Cobain')
    for database_record in query_result:
        print(database_record)
