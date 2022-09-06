import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src import types
from src.helpers.exceptions import PlaylistNotFoundError

from dotenv import load_dotenv

load_dotenv()

""" This is a wrapper around the spotipy module
	to give it more convenience features """

redirect_uri = 'http://localhost:8080/'
# redirect_uri = 'http://localhost/'
scope = ''
scope += 'playlist-read-private '
scope += 'playlist-modify-private '
scope += 'playlist-modify-public '
scope += 'playlist-read-collaborative'

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
		client_id=os.getenv('SPOTIPY_CLIENT_ID'),
		client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
		redirect_uri=redirect_uri, scope=scope))


def like_tracks(track_ids: list[str]):
	spotify.current_user_saved_tracks_add(track_ids)


def get_liked_tracks_generator(limit=50):
	""" returns a generator that loops over liked tracks
		in reverse chronological order.
		
		First item in first iteration
		is the most recently liked track. """
	# items: types.tracks.LikedTracksListDict | None
	offset = 0

	while True:
		items = spotify.current_user_saved_tracks(limit, offset)
		if items is None: continue
		items = types.tracks.LikedTracksListDict(items)
		# write_dict_to_file('liked_tracks', items)
		offset += limit

		yield items

		if not items.next:
			break


def get_one_playlist(playlist_id: str):
	""" should accept argument as uri, url and id """
	res = spotify.playlist(playlist_id)
	if res is None:
		raise PlaylistNotFoundError(f'Cannot find playlist with ID {playlist_id}')
	return types.playlists.SinglePlaylist(res)


def get_all_playlists():
	""" api call expense: 50 playlists = 1 call \n
			if one has 60 playlists in their spotify,
			this functions would do 2 api calls """


	all_playlists: list[dict] = []
	offset = 0

	while True:
		playlists: dict | None = spotify.current_user_playlists(offset=offset)

		if playlists is None:
			return []

		all_playlists += playlists['items']
		if playlists['next'] is None:
			break

		offset += 50
		# write_dict_to_file('current_user_playlists2', playlists)


	parsed_playlists = [
		types.playlists.AllPlaylists(playlist)
		for playlist in all_playlists
	]

	return parsed_playlists


