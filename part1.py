from database import query

# (3)  Skriv ut namnen på alla artister


def task3():
    artists_names = query('SELECT artists.name FROM artists', {})
    for artist in artists_names:
        print(artist[0])
# task3()

# (4) Skriv ut det äldsta albumet


def task4():
    oldest_album = query(
        'SELECT albums.title, MIN(albums.year_released) FROM albums', {})

    for album in oldest_album:
        print(f'Album: {album[0]}, Year: {album[1]}')
# task4()

# (5) Skriv ut albumet med längts speltid


def task5():
    longest_song = query('''
    SELECT al.title, SUM(so.duration) FROM albums AS al
    JOIN songs AS so
    ON al.id = so.album_id   
    GROUP BY al.title
    ORDER BY SUM(so.duration) DESC
    LIMIT 1
    ''')

    for song in longest_song:
        print(f'Album: {song[0]}, Duration: {song[1]} seconds')
# task5()

# (6) Uppdatera albumet som saknar year_released med ett årtal


def task6():
    album_list = query(
        'SELECT albums.title, albums.year_released FROM albums', {})

    for al in album_list:
        print(al['title'], al['year_released'])
    #query('UPDATE albums SET year_released = 2010 WHERE id = 7')
# task6()

# (7.1) Kunna skapa en artist


def task7x1():
    artist_name = input('name of artist: ')
    artist_des = input('description of artish ')
    query('''
    INSERT INTO artists VALUES (NULL, :name, :description)''',
          {'name': f'{artist_name}',
           'description': f'{artist_des}'
           }
          )
# task7x1()

# (7.2) Kunna skapa album till en artist


def task7x2():
    album_title = input('Title of album: ')
    album_des = input('Description of album: ')
    album_year = input('Year of released: ')
    album_thumbnail = input('Thumbnail of album: ')
    select_artist = query('SELECT artists.id, artists.name FROM artists', {})
    for artist in select_artist:
        print(artist[0], artist[1])
    album_artist = input('Artist of album: ')

    query('INSERT INTO albums VALUES (NULL, :title, :description, :year_released, :thumbnail, :artist_id)',
          {'title': album_title,
           'description': album_des,
           'year_released': album_year,
           'thumbnail': album_thumbnail,
           'artist_id': album_artist
           }
          )
# task7x2()

# (7.3) Kunna lägga till låtar i ett album


def task7x3():
    song_name = input('Name of song: ')
    song_duration = input('Duration of song: ')
    song_youtube_id = input('Youtube id of song: ')
    select_album = query('SELECT albums.id, albums.title FROM albums', {})
    print('Choose the album from the list below:')
    for album in select_album:
        print(album[0], album[1])
    song_album_id = input('Album id: ')

    query('INSERT INTO songs VALUES (NULL, :name, :duration, :youtube_id :album_id)',
          {'name': song_name,
           'duration': song_duration,
           'youtube_id': song_youtube_id,
           'album_id': song_album_id
           }
          )
# task7x3()

# (8) Kunna ta bort en artist, album eller låt via inmatning
# Tänk på: Om man tar bort en artist, borde dess album och låtar
# också tas bort då?

# delete song


def task8x1():
    print('What do you wanna do? choose from below:')
    choise1 = input('1. Delete song\n2. Delete album\n3. Delete artist ')

    if choise1 == '1':
        song_list = query('SELECT songs.id, songs.name FROM songs', {})
        for song in song_list:
            print(song[0], song[1])
        select_song = input('select an id for song to delete ')
        query('''
        DELETE FROM songs WHERE songs.id = :id
        ''',
              {'id': select_song}
              )
# task8x1()

# delete album: will also delete songs the album has


def task8x2():
    album_list = query('SELECT albums.id, albums.title FROM albums')

    for album in album_list:
        print(album['id'], album['title'])

    user_choice = int(input('choose an id for album to delete: '))
    query('''
    DELETE FROM albums WHERE albums.id = :aid
    ''',
          {'aid': user_choice}
          )

    album_list = query('SELECT albums.id, albums.title FROM albums')

    for album in album_list:
        print(album['id'], album['title'])

# task8x2()

# delete artist: will also delete all the albums and songs the artist has


def task8x3():
    artist_list = query('SELECT artists.id, artists.name FROM artists')

    for artist in artist_list:
        print(artist['id'], artist['name'])

    user_choice = int(input('choose an id for artist to delete '))

    query('''
    DELETE FROM artists WHERE artists.id = :aid
    ''',
          {'aid': user_choice}
          )

    artist_list = query('SELECT artists.id, artists.name FROM artists')

    for artist in artist_list:
        print(artist['id'], artist['name'])

# task8x3()


# (9) Skriv ut medel-längden på en låt i ett album
def task9():
    album_list = query('SELECT albums.id, albums.title FROM albums', {})
    for album in album_list:
        print(album[0], album[1])

    album_select = int(input('choose an album to get average length: '))
    song_average = query('''
    SELECT al.title, AVG(so.duration) FROM albums AS al
    JOIN songs AS so
    ON al.id = so.album_id
    WHERE al.id = :aid
    ''',
                         {'aid': album_select}
                         )

    for song in song_average:
        print(f'Song: {song[0]}, Duration: {song[1]} seconds')
# task9()

# (10) Visa den längsta låten från varje album


def task10():
    album_list = query('SELECT albums.id, albums.title FROM albums', {})
    for album in album_list:
        print(album[0], album[1])

    album_select = int(input('choose an album to get longest song: '))
    longest_song = query('''
    SELECT so.name, MAX(so.duration) FROM songs AS so
    JOIN albums AS al
    ON al.id = so.album_id
    WHERE al.id = :aid
    ''',
                         {'aid': album_select}
                         )

    for song in longest_song:
        print('song name:', song[0], ',',  'length:', song[1], 'min')
# task10()

# (11) Visa antal låtar varje artist har


def task11():
    artist_list = query('SELECT artists.id, artists.name FROM artists', {})
    for artist in artist_list:
        print(artist[0], artist[1])
    select_artist = int(input('select an artist id to get songs numbers: '))
    songs_number = query('''
    SELECT ar.name, COUNT(so.id) FROM artists AS ar
    JOIN albums AS al
    ON ar.id = al.artist_id
    JOIN songs AS so
    ON al.id = so.album_id
    WHERE ar.id = :arid
    ''',
                         {'arid': select_artist}
                         )
    for song in songs_number:
        print(song[0], ':', song[1], 'songs')
# task11()

# Kunna söka på artister via inmatning


def task12():
    find_artist = input('search an artist by name: ')

    select_artist = query('''
    SELECT * FROM artists WHERE name LIKE :search
    ''',
                          {'search': f'%{find_artist}%'}
                          )

    for artist in select_artist:
        print(artist[0], artist[1], artist[2])
# task12()

# Kunna söka på låtar via inmatning


def task13():
    song_name = input('find a song by name: ')

    find_song = query('''
    SELECT songs.id, songs.name FROM songs WHERE name LIKE :search
    ''',
                      {'search': f'%{song_name}%'}
                      )
    for song in find_song:
        print(song[0], song[1])
# task13()

# Kunna visa detaljer om en artist där man även ser artistens alla album


def task14():
    artist_details = query('''
    SELECT ar.*, GROUP_CONCAT(al.title, ',  ') FROM artists AS ar
    JOIN albums AS al
    ON ar.id = al.artist_id
    GROUP BY ar.id, ar.name, ar.description
    
    ''', {})
    for artist in artist_details:
        print(artist[0], artist[1], '(', artist[2], ')',
              ' Albums: ', artist[4])

# task14()

# (15) Kunna visa detaljer om ett album där man även ser albumets låtar
# (16) Detaljsidan för en artist och album visar även hur många låtar varje album har, och total speltid för ett album


def task15and16():
    album_list = query('SELECT albums.id, albums.title FROM albums')
    for album in album_list:
        print(album[0], album[1])

    ask_user = int(input('select an album by its id to get the songs list '))

    select_album = query('''
    SELECT al.title, al.description, GROUP_CONCAT(so.name, ', '), COUNT(so.album_id), SUM(so.duration) FROM albums AS al
    JOIN songs AS so
    ON al.id = so.album_id
    WHERE al.id = :aid
    GROUP BY al.title, al.description
    ''',
                         {'aid': ask_user}
                         )

    for album in select_album:
        print(album[0], '(', album[1], ')', 'Songs:', album[2],
              '(Total song:', album[3], 'Total duration:', album[4], 'seconds)')

# task15and16()

# (17) Gör så att alla listor går att sortera på olika egenskaper, som name, year_released eller duration


def task17():
    sort_list = query('''
    SELECT al.title, al.description, al.year_released, GROUP_CONCAT(so.name, ', '), COUNT(so.album_id), SUM(so.duration) FROM albums AS al
    JOIN songs AS so
    ON al.id = so.album_id
    GROUP BY al.title, al.description
    ORDER BY al.title_released;
    ''')
    # ORDER BY al.year_released;
    # ORDER BY SUM(so.duration);

    for item in sort_list:
        print(item[0], item[1], item[2], item[3], item[4], item[5])
# task17()
