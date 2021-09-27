# 2021 S2 COMPSCI235 Lab 5 - SQLite Databases

Lab Report for Lab 5 COMPSCI235 - SQLite Databases

Question ONE:
- I utilized the sqlite3 module by calling the 'connect' function in order to establish a connection to a specified database (in this case, chinook.db).
- A dictionary is created to hold information from the database (a dictionary is good to hold data like this because it can store mappings of unique keys to different values). A list may be similar but is not recommended due to the need to specifically and manually pair a value with another while a dictionary bypasses that and is easier to parse.
- I obtained a cursor from the connection (a cursor is a temporary work area in which SQL statements and queries can be executed). In this case, I have set a cursor with the connection to the database, and then told the cursor object to execute a specific SQL query ("SELECT name FROM sqlite_master WHERE type='table').
- This then returns the result from the query.
- I then created a list to hold all of the table names (table names were obtained from the query specifying to return table names column).
- Due to the format of the result, any rows that start with sqlite will not be read, while all others will be read and appended to create a list of all the table names.
- I think stmt can be done using f' strings instead:
    `stmt = f"PRAGMA table_info('{table_name}')"`
- The following lines then attempt to populate the dictionary with the results in the list.
- It first grabs all the values in each table_name. Then, using what it grabbed, goes into a for-loop that looks at the table_name, checks if it exists (if it doesn't, create it, then append the value to it), and loops through it to append all values to its appropriate table_name.

Question TWO:
- Since we want all data values, we will set stmt to the specific query:
    `stmt = f"SELECT * FROM {table_name}"
	Note: '*' means it will select all fields available in the table (table_name).
	
Question THREE:
- First, I used the copied code to establish the dictionary.
- Then I did a pre-check to see if the column exists, otherwise return empty list (for pytest test_cases).
- Copied some of the code from Q1 so that I don't need to retype.
- Modified stmt once again to grab relevant data values from the table. As the question specifies to get any value with "Greatest Hits" and or "Best Of" in a specific table, I looked up some syntax for SQL database queries.
- Looking up syntax, I tried my first query attempt:
    `stmt = f"SELECT * FROM albums WHERE Title Like 'Greatest Hits' OR Title Like 'Best Of' ORDER BY {{column_name_for_ordering})`
- It turns out I missed a very important syntax issue that requires the use of the '%' (or LIKE) operator:
    `stmt = f"SELECT * FROM albums WHERE Title Like '%Greatest Hits%' OR Title Like '%Best Of%' ORDER BY {{column_name_for_ordering})`
- This tells the execution to look for a specified pattern (in this case, data values with that exact string).

Question FOUR:
- I tried following an INNER JOIN example, and ended up with:
    `stmt = "SELECT AL.AlbumId, AL.Title,AR.name \
    FROM albums AL JOIN artists AR ON AL.ArtistId = AR.ArtistId \
    WHERE AL.Title LIKE '%Greatest Hits%' OR AL.Title \
    LIKE '%Best Of%' ORDER BY AR.Name"`
- It turned out to work, but now I'm wondering if there is a better way to write this.

Question FIVE:
- I copied the code from Q4, and modified the query as to include the new restrictions:
    `stmt = "SELECT AR.ArtistId AS 'Artist ID' \
			AR.name AS 'Artist name' \
			count(AL.AlbumId) AS 'Number of albums' \
            FROM albums AL JOIN artists AR ON AL.ArtistId = AR.ArtistId \
    NEW ->  GROUP BY AR.name \
            HAVING count(AL.AlbumId) >= " + str(n) + " \
            ORDER BY count(AL.AlbumId) DESC, AR.name ASC"`
			
Question SIX:
- From Q1, I borrowed the code skeleton to create an initial query:
    `stmt = f"SELECT PlaylistId, Name FROM playlists WHERE Name='{which_playlist}'"`
- I then did a bunch of INNER JOIN as previous questions to come up with this:
    `playlist_stmt = f"SELECT tracks.Name, album.Title, genre.Name, artist.Name, tracks.Composer FROM tracks \
                INNER JOIN albums album ON tracks.AlbumId=album.AlbumId \
                INNER JOIN genres genre ON tracks.GenreId=genre.GenreId \
                INNER JOIN artists artist ON album.ArtistId=artist.ArtistId \
                INNER JOIN playlist_track pt ON pt.PlaylistId = {playlist_id} \
                WHERE tracks.TrackId = pt.TrackId ")`
- Sorted by default track
