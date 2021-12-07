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


@app.get('/details/<int:uid>')
# get a dynamic parameter 'removeid'. (always a string)
def details(uid):
    artists = query('''
        SELECT artists.*, albums.*, albums.id AS album_id, albums.thumbnail AS album_thumbnail, 
        SUM(songs.duration/60) AS duration, COUNT(songs.id) AS song_count FROM artists
        LEFT JOIN albums
        ON artists.id= albums.artist_id
        JOIN songs
        ON albums.id = songs.album_id
        WHERE artists.id= :id
        GROUP BY album_id
        ''', {
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
                'album_id' : row['album_id'],
                'title': row['title'],
                'year_released': row['year_released'],
                'thumbnail': row.get('album_thumbnail'),
                'duration' : row['duration'],
                'song_count' : row['song_count']
            })

    artists = list(artists_info.values())
    return render_template('details.html', artist=artists[0])


@app.get('/info/<int:aid>')
# get a dynamic parameter 'removeid'. (always a string)
def album_info(aid):

    artists = query('''
        SELECT artists.*, albums.*, albums.id AS album_id, albums.thumbnail AS album_thumbnail, 
        GROUP_CONCAT(songs.name, ', ') AS song_name, songs.youtube_id,
        SUM(songs.duration/60) AS duration, COUNT(songs.id) AS song_count FROM artists
        LEFT JOIN albums
        ON artists.id= albums.artist_id
        JOIN songs
        ON albums.id = songs.album_id
        WHERE artists.id= :id
        GROUP BY album_id
        ''', {
        'id': aid
    })

    artists_info = {}

    for row in artists:
        row = dict(row)

        

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
                'album_id': row['album_id'],
                'title': row['title'],
                'year_released': row['year_released'],
                'thumbnail': row.get('album_thumbnail'),
                'duration' : row['duration'],
                'song_count' : row['song_count'],
                'songs' : []
                
            })

        if row['youtube_id'] != None:
            artists_info[id]['albums'][id]['songs'].append({
            'song_name' : row['song_name']
        })

             

            

    albums = list(artists_info.values())
    return render_template('info.html', artist=albums[1])


if __name__ == '__main__':
    app.run(debug=True)
