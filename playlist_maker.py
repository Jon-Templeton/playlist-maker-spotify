# Playlist maker by Jon

import json
import spotipy
import random
import time
import spotipy.util as util
from json.decoder import JSONDecodeError

try:
    # Enter your information for client_id and client_secret (as a str)
    spotipy_client_id = ''
    spotipy_client_secret = ''

    print()
    print(">> Welcome to Jon's Playlist Maker!")

    username = input('>> What is your username: ')
    scope = 'user-read-private playlist-read-collaborative playlist-modify-public user-top-read playlist-read-private playlist-modify-private'

    # Prompt for user permission
    token = util.prompt_for_user_token(username, scope, spotipy_client_id, spotipy_client_secret, 'http://google.com/')

    # Spotify Object
    spotifyObject = spotipy.Spotify(auth=token)

    # User info
    user = spotifyObject.current_user()
    displayName = user['display_name']
    user_id = user['id']

    print()
    print(f'Hello {displayName}')
    print("Please name the model playlist 'trainer'")
    choice = input("Enter 'y' to continue, 'x' to quit: ")
    choice = choice.lower()

    # Main Program
    if choice == 'y':
        print()

        # Find Trainer Playlist and Trainer ID
        try: 
            userPlaylists = spotifyObject.current_user_playlists()
            trainer_name = ''
            i = -1
            while trainer_name != 'trainer':
                i += 1
                trainer_name = userPlaylists['items'][i]['name']

            trainer_id = userPlaylists['items'][i]['id']
            print('>> Playlist Found')

            # Find songs, song ID, artist, artist ID in trainer playlist
            songs_in_trainer = spotifyObject.playlist_tracks(trainer_id)
            trainer_song_names = []
            trainer_song_id = []
            trainer_song_artist = []
            trainer_artist_id = []
            j = -1
            for song in songs_in_trainer['items']:
                j += 1
                trainer_song_names.append(songs_in_trainer['items'][j]['track']['name'])
                trainer_song_id.append(songs_in_trainer['items'][j]['track']['id'])
                trainer_song_artist.append(songs_in_trainer['items'][j]['track']['artists'][0]['name'])
                trainer_artist_id.append(songs_in_trainer['items'][j]['track']['artists'][0]['id'])
            
            # Find genres from trainer artists
            trainer_genres_full = []
            for artist in trainer_artist_id:
                trainer_artist_artist = spotifyObject.artist(artist)
                z = -1
                for genre in trainer_artist_artist['genres']:
                    z += 1
                    trainer_genres_full.append(trainer_artist_artist['genres'][z])

            print(f">> Songs in 'trainer': {len(trainer_song_names)}")

            # Create genre list that is acceptable
            possible_genre_seeds = spotifyObject.recommendation_genre_seeds()
            possible_genre_seeds =  ['acoustic', 'afrobeat', 'alt rock', 'alternative', 'ambient', 'anime', 'black metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death metal', 'deep house', 'detroit techno', 'disco', 'disney', 'drum and bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard rock', 'hardcore', 'hardstyle', 'heavy metal', 'hip hop', 'holidays', 'honky tonk', 'house', 'idm', 'indian', 'indie', 'indie pop', 'industrial', 'iranian', 'j dance', 'j idol', 'j pop', 'j rock', 'jazz', 'k pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal misc', 'metalcore', 'minimal techno', 'movies', 'mpb', 'new age', 'new release', 'opera', 'pagode', 'party', 'philippines opm', 'piano', 'pop', 'pop film', 'post dubstep', 'power pop', 'progressive house', 'psych rock', 'punk', 'punk rock', 'rnb', 'rainy day', 'reggae', 'reggaeton', 'road trip', 'rock', 'rock n roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth pop', 'tango', 'techno', 'trance', 'trip hop', 'turkish', 'work out', 'world music']
            trainer_genre_seeds = []

            for inputs in trainer_genres_full:
                for genre in possible_genre_seeds:
                    result = genre in inputs
                    if result == True:
                        trainer_genre_seeds.append(genre)         
                    
            # Get recommendations

            # Recommendations per song
            rec_song_names = []
            rec_song_id = []
            new_playlist_length = int(input('>> How many new songs do you want: '))
            print()
            print('Making new playlist...')
            if len(trainer_song_names) <= new_playlist_length:
                rec_per_song = new_playlist_length // len(trainer_song_names)
                remainder_songs = new_playlist_length % len(trainer_song_names)
                print()

                for song in trainer_song_id:
                    for rec in range(0, rec_per_song):
                        rand_genre1 = trainer_genre_seeds[random.randint(0, len(trainer_genre_seeds)-1)]
                        rand_genre2 = trainer_genre_seeds[random.randint(0, len(trainer_genre_seeds)-1)]
                        rand_artist1 = trainer_artist_id[random.randint(0, len(trainer_artist_id)-1)]
                        rand_artist2 = trainer_artist_id[random.randint(0, len(trainer_artist_id)-1)]
                        rec_data = spotifyObject.recommendations([rand_artist1, rand_artist2], [rand_genre1, rand_genre2], [song], 1)
                        rec_song_names.append(rec_data['tracks'][0]['name'])
                        rec_song_id.append(rec_data['tracks'][0]['id'])
                
                while remainder_songs != 0:
                    rand_artist1 = trainer_artist_id[random.randint(0, len(trainer_artist_id)-1)]
                    rand_artist2 = trainer_artist_id[random.randint(0, len(trainer_artist_id)-1)]
                    rand_genre1 = trainer_genre_seeds[random.randint(0, len(trainer_genre_seeds)-1)]
                    rand_genre2 = trainer_genre_seeds[random.randint(0, len(trainer_genre_seeds)-1)]
                    rand_song = trainer_song_id[random.randint(0, len(trainer_song_id)-1)]
                    rec_data = spotifyObject.recommendations([rand_artist1, rand_artist2], [rand_genre1, rand_genre2], [rand_song], 1)
                    rec_song_names.append(rec_data['tracks'][0]['name'])
                    rec_song_id.append(rec_data['tracks'][0]['id'])
                    remainder_songs -= 1

            # If trainer playlist length > length of new playlist
            else:
                for song in range(0, new_playlist_length):
                    rand_artist1 = trainer_artist_id[random.randint(0, len(trainer_artist_id)-1)]
                    rand_artist2 = trainer_artist_id[random.randint(0, len(trainer_artist_id)-1)]
                    rand_genre1 = trainer_genre_seeds[random.randint(0, len(trainer_genre_seeds)-1)]
                    rand_genre2 = trainer_genre_seeds[random.randint(0, len(trainer_genre_seeds)-1)]
                    rand_song = trainer_song_id[random.randint(0, len(trainer_song_id)-1)]
                    rec_data = spotifyObject.recommendations([rand_artist1, rand_artist2], [rand_genre1, rand_genre2], [rand_song], 1)
                    rec_song_names.append(rec_data['tracks'][0]['name'])
                    rec_song_id.append(rec_data['tracks'][0]['id'])
            
            print()
            print(f'New Songs: {rec_song_names}')

            # Make new playlist
            
            # Search for JayTee Recommendations Playlist
            userPlaylists = spotifyObject.current_user_playlists()       
            i = -1
            for playlist in userPlaylists['items']:
                i += 1
                if userPlaylists['items'][i]['name'] == 'JayTee Recommendations':
                    has_rec_playlist = True
                    rec_playlist_id = userPlaylists['items'][i]['id']
                    spotifyObject.user_playlist_replace_tracks(user_id, rec_playlist_id, rec_song_id)
                    break
                else:
                    has_rec_playlist = False

            # If 'JayTee Recommendations' doesnt exist
            if has_rec_playlist == False:
                # make new playlist 'JayTee Recommendations'
                spotifyObject.user_playlist_create(user_id, 'JayTee Recommendations', description="Songs recommended by JayTee and based of your 'trainer' playlist, run program for new recommendations")
                # Get id of JayTee Recommendations playlist
                time.sleep(2)
                userPlaylists = spotifyObject.current_user_playlists()
                has_playlist = ''
                i = -1
                while has_playlist != 'JayTee Recommendations':
                    i += 1
                    has_playlist = userPlaylists['items'][i]['name']
                rec_playlist_id = userPlaylists['items'][i]['id']        
                # Add songs to JayTee Recommendations playlist
                spotifyObject.user_playlist_add_tracks(user_id, rec_playlist_id, rec_song_id)
            
            print()
            print("Thanks for using Jon's Playlist Maker")

        except IndexError:
            print("Error! Could not find playlist, please name playlist 'trainer' and re-run program")
            
    elif choice == 'x':
        print("Thanks for using Jon's Playlist Maker")
        
except spotipy.exceptions.SpotifyException:
    print('>> Please add your client_id and client_secret to the top of the code')