from src.tracks import Tracks
from src.playlists.live_playlists import LivePlaylists
from src import sp

playlist_songs = ['33Axn97y8NTI3EQfUkMtA4', '1CFlJQumKNMHB9o634moJ9', '3zL5wXTu2usPr2Ovwkt5m6', '6NHQNFSpBaBvTHTt96dhfy', '0BhCK7Z9fg4cqu0q0gNtjT', '2Z4kEzYRGKCKRv9QttvBrW', '5KbxqOKDWG085zmuTn7qsa', '2Ucd1gHdGTBc90QgWgcUN5', '0YGPY8ivoYZwBe95b5AcmH', '13KLstO6ywva9h94FOqpeW', '2xeW5CIB5XHkaDLYEFOSjs', '5PF2WtSZV4EtmGx4oER1zt', '2VvohoUXfl1dW6gM1UHPvK', '0HX7Qdf2R0pfeDueFpF6C4', '3Yojk6oNOGZGlxMrYXsaJh', '3A6WcOcwVB3dFZppYvlEvi', '0euC0zrWPMPACwjnyulC6l', '6WoloXr2PXu8FRYZFtzbij', '4qDVck33icBULgnvP6WmPh', '6CRrPTcxzM4pIO29GJF7Nk', '2KnuaZYoGzDoHiBTNYOTXG', '0FfqyjhB6Kspvit1oOo7ax', '2EZemIRw1LnIUM7YoiKWPQ', '7r8SEXh79XwN1tmOG2dbxN', '4dDEkdgT6gLXG1VSI0Qgtq', '02zYabT1FTwMy8byKpd40O', '6XR59BEFC1Z2kQ7PayDNPj', '7u2PsDpp4FdXsbn4sTh6MY', '5EMGQPQI60jvyDjKT2Fn2I', '6rSUrh8ErKSKfbH0t0IzCM', '6UdoWvHXqS0T4j0qCFFxBl', '0VMmHFqENPTDq3lHafvOPt', '2hNBhYGXQbq9KHYvK2itFY', '7x0vY5vTKzxMqozQWCj8Nd', '6dquCx5KAW5jCgGgoTlghL', '1IY1Ge6tFl0m9pr2Yg0OFe', '4jPr49jXRJHftXlwTEA2w4', '7kTlyuaUciX2wQx7ogrd9w', '3j57f5yEpiLZYgkcA1GKjc', '7B76OJ0ExVlSkDh1xelvRl', '2aLH4EiEoZLpbeEQvTBbtH', '1USo158Kncaxfyq9q306dn', '0DXZHcAQAkXx8YlMIdzqgG', '7ycZN2o5PMNuTkUg2Q73wN', '0dNN5wjTkbJnQkOnzh9WUH', '6xS02EfbvnneFWCM90PJFG', '69jstgacdd40OwG9cLl45r', '3wdkrgUEyjhUSNSMV7cWgP', '2hmn4VOZepYRxdw7vKyagU', '6OZ3FzEORUBi1lvU4EfypC']
playlist_songs.reverse()
archive_playlist_songs = []
archive_playlist_songs.reverse()


def reset():
	playlists = LivePlaylists()

	playlist = playlists.get_by_name('Playlist')
	archive_playlist = playlists.get_by_name('Archive Playlist')

	sp.replace_playlist_tracks(playlist.uri, playlist_songs)
	sp.replace_playlist_tracks(archive_playlist.uri, archive_playlist_songs)
	# playlist.replace_tracks(playlist_songs)
	# archive_playlist.replace_tracks(archive_playlist_songs)


def get_tracks():
	playlists = LivePlaylists()

	playlist = playlists.get_by_name('Calm')

	tracks = playlist.get_latest_tracks(None)

	print(Tracks.get_ids(tracks))