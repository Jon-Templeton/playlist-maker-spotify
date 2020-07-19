#Playlist Maker 2.0 by Jon w/ GUI
import tkinter as tk
from tkinter import font
import json
import spotipy
import random
import time
import requests
from tkinter import font
import spotipy.util as util
import os.path
from os import path
from json.decoder import JSONDecodeError

height = 500
width = 600
scope = 'user-read-private playlist-read-collaborative playlist-modify-public user-top-read playlist-read-private playlist-modify-private'

# Tkinter main loop
root = tk.Tk()

def onPress(event):
    enter_info(info1_entry.get(), info2_entry.get())

def onPress2(event):
    makePlaylist(songs_entry.get())

def onPress3(event):
    saveInfo(spotipy_client_id, spotipy_client_secret)

def changeInfo():
    frame3.pack_forget()
    frame1.pack()

def changeUser(spotipy_client_id, spotipy_client_secret):
    root.bind('<Return>', onPress3)
    frame3.pack_forget()
    global frame4
    frame4 = tk.Frame(root, height=height, width=width, bg='#262626')
    frame4.pack()
    logo_label = tk.Label(frame4, image=logo)
    logo_label.place(relx=0.02, rely=0.02, relwidth=0.265, relheight=0.113,)
    user_border_frame = tk.Frame(frame4, bd=4)
    user_border_frame.place(anchor='n', relx=0.5, rely=0.35, relwidth=0.69, relheight=0.1)
    welcome_label = tk.Label(user_border_frame, text="To Change User, Log-out of Spotify \nfrom your web browser and continue", font=('Courier', 14), fg='white', bg='#262626')
    welcome_label.place(anchor='w',rely=0.5, relheight=1, relwidth=1)
    enter_button = tk.Button(frame4, text='Continue', font=('Courier',13), bg='#ff914d', fg='black', command=lambda: saveInfo(spotipy_client_id, spotipy_client_secret))
    enter_button.place(anchor='n', relx=0.5, rely=0.55)
    try:
        os.remove('.cache-username')
    except:
        pass

def enter_info(info1, info2):
    root.bind('<Return>', onPress2)
    if (len(info1) < 2) or (len(info2) < 2):
        error_label = tk.Label(frame1, text='Missing Information', font=('Courier',12), bg='#262626', fg='red')
        error_label.place(anchor='n', relx=0.5, rely=0.7)
    elif (len(info1) > 2) and (len(info2) > 2):
        error_label = tk.Label(frame1, text='Missing Information', font=('Courier',12), bg='#262626', fg='#262626')
        error_label.place(anchor='n', relx=0.5, rely=0.7)    

        saveInfo(info1, info2)

def saveInfo(spotipy_client_id, spotipy_client_secret):
    root.bind('<Return>', onPress2)
    # Creates dictionary with information
    data = {}
    data['user info'] = {'client id': spotipy_client_id, 'client secret': spotipy_client_secret}
    # Save data in JSON
    with open('userinfo.json', 'w') as f:
        json.dump(data, f)
    global token
    # Prompt for user permission
    token = util.prompt_for_user_token('username', scope, spotipy_client_id, spotipy_client_secret, 'http://localhost:8080')
    songSelect()

def songSelect():
    frame1.pack_forget()
    try:
        frame3.pack_forget()
    except:
        pass
    try:
        frame4.pack_forget()
    except:
        pass
    global frame2
    frame2 = tk.Frame(root, height=height, width=width, bg='#262626')
    frame2.pack()
    logo_label = tk.Label(frame2, image=logo)
    logo_label.place(relx=0.02, rely=0.02, relwidth=0.265, relheight=0.113,)
    songs_border_frame = tk.Frame(frame2, bd=3)
    songs_border_frame.place(anchor='n', relx=0.5, rely=0.3, relwidth=0.92, relheight=0.15)
    songs_bgframe1 = tk.Frame(songs_border_frame, bd=3, bg='#262626')
    songs_bgframe1.place(relwidth=1, relheight=1)
    songs_label = tk.Label(songs_bgframe1, text='Songs in new playlist:', font=('Courier',12), bg='#262626', fg='white')
    songs_label.place(anchor='w', relx=.01, rely=0.5)
    trainer_label = tk.Label(frame2, text="Name Model Playlist 'trainer'", font=('Courier',14), bg='#262626', fg='white')
    trainer_label.place(anchor='n', relx=.5, rely=0.22)
    songs_frame = tk.Frame(songs_bgframe1, bd=2.4, bg='#f2f2f2')
    songs_frame.place(anchor='w', relx=0.44, rely=0.5, relwidth=0.11, relheight=0.4)
    global songs_entry
    songs_entry = tk.Entry(songs_frame, font=('Courier',13), bg='#4d4d4d', fg='white', justify='center')
    songs_entry.place(anchor='w', rely=0.5, relwidth=1, relheight=1)
    songs_scale = tk.Scale(songs_bgframe1, bg='#4d4d4d', takefocus=0, from_=0, to=30, orient='horizontal', length = 200, width=14, sliderlength=30, showvalue=0, tickinterval=10, command=scaleUpdate)
    songs_scale.set(15)
    songs_scale.place(anchor='w', relx=0.6, rely=0.5)
    songs_button = tk.Button(frame2, text='Enter', font=('Courier',13), bg='#ff914d', fg='black', command=lambda: makePlaylist(songs_entry.get()))
    songs_button.place(anchor='n', relx=0.5, rely=0.75)

def scaleUpdate(value):
    songs_entry.delete(0, last=20)
    songs_entry.insert(0, value)


def makePlaylist(number):
    global error_label2
    global error_label3
    try:
        # Removes Error Labels
        error_label2 = tk.Label(root, text='Error! Whole Numbers Only', font=('Courier',12), bg='#262626', fg='#262626')
        error_label2.place(anchor='n', relx=0.5, rely=0.65)
        error_label3 = tk.Label(root, text="Error! Could Not Find Playlist, Please name playlist 'trainer'", font=('Courier',11), bg='#262626', fg='#262626')
        error_label3.place(anchor='n', relx=0.5, rely=0.6)
        number = int(number)
        # Spotify Object
        spotifyObject = spotipy.Spotify(auth=token)
        # User info
        user = spotifyObject.current_user()
        displayName = user['display_name']
        user_id = user['id']
        # Main Program
        # Find Trainer Playlist and Trainer ID
        try: 
            userPlaylists = spotifyObject.current_user_playlists()
            trainer_name = ''
            i = -1
            while trainer_name != 'trainer':
                i += 1
                trainer_name = userPlaylists['items'][i]['name']

            trainer_id = userPlaylists['items'][i]['id']

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
            new_playlist_length = number
            if len(trainer_song_names) <= new_playlist_length:
                rec_per_song = new_playlist_length // len(trainer_song_names)
                remainder_songs = new_playlist_length % len(trainer_song_names)
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
                userPlaylists = spotifyObject.current_user_playlists()
                has_playlist = ''
                i = -1
                while has_playlist != 'JayTee Recommendations':
                    i += 1
                    has_playlist = userPlaylists['items'][i]['name']
                rec_playlist_id = userPlaylists['items'][i]['id']        
                # Add songs to JayTee Recommendations playlist
                spotifyObject.user_playlist_add_tracks(user_id, rec_playlist_id, rec_song_id)

        except IndexError:
            error_label3 = tk.Label(root, text="Error! Could Not Find Playlist, Please name playlist 'trainer'", font=('Courier',11), bg='#262626', fg='red')
            error_label3.place(anchor='n', relx=0.5, rely=0.6)
            
    except:
        error_label2 = tk.Label(root, text='Error! Whole Numbers Only', font=('Courier',12), bg='#262626', fg='red')
        error_label2.place(anchor='n', relx=0.5, rely=0.65)

root.bind('<Return>', onPress)
root.title('Playlist Maker 2.0')
root.minsize(300,300)
root.maxsize(width, height)
root.configure(bg='#262626')

frame1 = tk.Frame(root, height=height, width=width, bg='#262626')
frame1.pack()
logo = tk.PhotoImage(file='logo.png')
logo_label = tk.Label(frame1, image=logo)
logo_label.place(relx=0.02, rely=0.02, relwidth=0.265, relheight=0.113,)
welcome_label = tk.Label(frame1, text="Welcome to Jon's Playlist Maker!", font=('Courier', 15), fg='white', bg='#262626')
welcome_label.place(anchor='n', relx=0.5, rely=0.2, relwidth=.65)
dev_label = tk.Label(frame1, text='Enter Info from Spotify Developer Account Below:', font=('Courier', 12), fg='white', bg='#262626')
dev_label.place(anchor='n', relx=0.5, rely=0.4, relwidth=.8)
info1_label = tk.Label(frame1, text='Client ID:', font=('Courier',12), bg='#262626', fg='white')
info1_label.place(anchor='ne', relx=.35, rely=0.5)
info1_frame = tk.Frame(frame1, bd=3, bg='#f2f2f2')
info1_frame.place(anchor='n', relx=0.56, rely=0.5, relwidth=0.4, relheight=0.06)
info1_entry = tk.Entry(info1_frame, font=('Courier',12), bg='#4d4d4d', fg='white')
info1_entry.place(anchor='w', rely=0.5, relwidth=1, relheight=1)
info2_label = tk.Label(frame1, text='Client Secret:', font=('Courier',12), bg='#262626', fg='white')
info2_label.place(anchor='ne', relx=.35, rely=0.6)
info2_frame = tk.Frame(frame1, bd=3, bg='#f2f2f2')
info2_frame.place(anchor='n', relx=0.56, rely=0.6, relwidth=0.4, relheight=0.06)
info2_entry = tk.Entry(info2_frame, font=('Courier',12), bg='#4d4d4d', fg='white')
info2_entry.place(anchor='w', rely=0.5, relwidth=1, relheight=1)
enter_button = tk.Button(frame1, text='Enter', font=('Courier',13), bg='#ff914d', fg='black', command=lambda: enter_info(info1_entry.get(), info2_entry.get()))
enter_button.place(anchor='n', relx=0.5, rely=0.75)

try:
    # If previous user, find json file
    f = open('userinfo.json')
    data = json.load(f)
    spotipy_client_id = data['user info']['client id']
    spotipy_client_secret = data['user info']['client secret']

    global frame3
    frame1.pack_forget()
    frame3 = tk.Frame(root, height=height, width=width, bg='#262626')
    frame3.pack()
    logo_label = tk.Label(frame3, image=logo)
    logo_label.place(relx=0.02, rely=0.02, relwidth=0.265, relheight=0.113,)
    welcome_border_frame = tk.Frame(frame3, bd=4)
    welcome_border_frame.place(anchor='n', relx=0.5, rely=0.35, relwidth=0.69, relheight=0.08)
    welcome_label = tk.Label(welcome_border_frame, text="Welcome to Jon's Playlist Maker!", font=('Courier', 15), fg='white', bg='#262626')
    welcome_label.place(anchor='w',rely=0.5, relheight=1, relwidth=1)
    enter_button = tk.Button(frame3, text='Enter', font=('Courier',13), bg='#ff914d', fg='black', command=lambda: saveInfo(spotipy_client_id, spotipy_client_secret))
    enter_button.place(anchor='n', relx=0.5, rely=0.55)
    change_button = tk.Button(frame3, text='Change Dev Info', font=('Courier',8), bg='grey', fg='black', command=lambda: changeInfo())
    change_button.place(anchor='ne', relx=0.98, rely=0.02)
    user_button = tk.Button(frame3, text='Change User', font=('Courier',8), bg='grey', fg='black', command=lambda: changeUser(spotipy_client_id, spotipy_client_secret))
    user_button.place(anchor='ne', relx=0.98, rely=0.08)
    root.bind('<Return>', onPress3)

    info1_entry.insert(0, spotipy_client_id)
    info2_entry.insert(0, spotipy_client_secret)
except:
    pass

root.mainloop()