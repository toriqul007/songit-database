from database import query
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


artists = query('''
        SELECT artists.id, artists.name, artists.description, artists.thumbnail, GROUP_CONCAT(albums.title, ',  ') AS ALBUM
        FROM artists, albums
        WHERE artists.id= albums.artist_id
        GROUP BY artists.name, artists.description, artists.thumbnail;
    ''')


@app.get('/')
def index():

    return render_template('index.html', artists=artists)


""" @app.get('/details/<int:detailid>')
# get a dynamic parameter 'removeid'. (always a string)
def details(detailid):

    for artist in artists:
        # runnig the loop method  to get all the elements
        if artist['id'] == detailid:
            # if randomly generated 'movie id' matches with the 'form movie id',then it removes
            # remove elements(movie) from the list with remove() mehtod
            return render_template('details.html', artist=artist)

    # keep user on the same page
 """

""" @app.get('/info')
def info(id):
    db_albums = query('''
        SELECT * FROM artists
        LEFT JOIN albums
        ON artists.id= albums.artist_id
        WHERE artists.id= :id''', {
        'id': int(id)
    })

    artists = {}

    for row in db_albums:
        print(row['id'], row['name'], row['description'])

        id = row['id']

# create row if not exists
        if artists.get(id) == None:
            artists[id] = {
                'name': row['name'],
                'description': row['description'],
                'albums': []
            }
# add album to artist (if there is a album)
        if row['title'] != None:
            artists[id]['albums'].append({
                'title': row['title'],
                'description': row['description'],
                'year_released': row['year_released']
            })

            return render_template('info.html', artist=db_albums)
 """


@app.get('/details/<int:uid>')
# get a dynamic parameter 'removeid'. (always a string)
def details(uid):
    artists = query('''
        SELECT artists.*, albums.*,albums.id AS album_id,albums.thumbnail AS album_thumbnail, 
        SUM(songs.duration/60) AS album_duration_min, COUNT(songs.id) AS song_numbers FROM artists
        LEFT JOIN albums
        ON artists.id= albums.artist_id
        JOIN songs
        ON albums.id= songs.album_id
        WHERE artists.id=id''', {
        'id': uid
    })

    artists_info = {}

    for row in artists:
        row = dict(row)

        print(row['name'])

        id = row['id']

# create row if not exists
        if artists_info.get(id) == None:
            artists_info[id] = {
                'name': row['name'],
                'description': row['description'],
                'thumbnail': row['thumbnail'],
                'albums': []
            }

# add album to artist (if there is a album)
        if row['title'] != None:
            artists_info[id]['albums'].append({
                # add album id
                'id': row['id'],
                'title': row['title'],
                'year_released': row['year_released'],
                'thumbnail': row.get('album_thumbnail')
            })

    artists = list(artists_info.values())
    return render_template('details.html', artist=artists[0])


@app.get('/info/<int:aid>')
# get a dynamic parameter 'removeid'. (always a string)
def album_info(id):
    albums = query('''
        SELECT songs.*
        FROM albums
        LEFT JOIN songs
        ON albums.id= songs.album_id
        WHERE albums.id= :id''', {
        'id': id
    })

    albums_info = {}

    for row in albums:
        row = dict(row)

        #print(row['name'])

        id = row['id']

# create row if not exists
        if albums_info.get(id) == None:
            albums_info[id] = {
                'title': row['title'],
                'description': row['description'],
                'year_released': row['year_released'],
                'thumbnail': row.get('album_thumbnail'),
                'songs ': []
            }

# add album to artist (if there is a album)
        if row['title'] != None:
            albums_info[id]['songs'].append({
                'title': row['title'],
                'year_released': row['year_released'],
                'thumbnail': row.get('album_thumbnail')
            })

    albums = list(albums_info.values())
    return render_template('info.html', album=albums[0])


if __name__ == '__main__':
    app.run(debug=True)
