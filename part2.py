from database import query
from flask import Flask, render_template, redirect

app = Flask(__name__, static_folder='static', static_url_path='')

# artists = query('''
# SELECT * FROM artists
# ''')

artists = query('''
SELECT ar.id, ar.name, ar.description, ar.thumbnail, 
GROUP_CONCAT(al.title, al.thumbnail)
FROM artists AS ar
JOIN albums AS al
ON ar.id = al.artist_id
GROUP BY ar.name, ar.description, ar.thumbnail
''')

artist_detail = query('''
SELECT * FROM artists
LEFT JOIN albums
ON artists.id = albums.artist_id
''')


@app.get('/')
def index():
    return render_template('index.html', artists=artists)


@app.get('/details/<int:uid>')
# get a dynamic parameter 'uid'. (always a string)
def details(uid):
    artists = query('''
        SELECT artists.*, albums.*, albums.thumbnail AS album_thumbnail, COUNT(songs.id) AS Total_song FROM artists
        LEFT JOIN albums
        ON artists.id= albums.artist_id
        JOIN songs
        ON albums.id = songs.album_id
        WHERE artists.id= :id
        GROUP BY artists.name, albums.title''', {
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
                'title': row['title'],
                'year_released': row['year_released'],
                'thumbnail': row.get('album_thumbnail')

            })

    artists = list(artists_info.values())
    return render_template('details.html', artist=artists[0])

# to run the flask app
app.run(debug=True)
