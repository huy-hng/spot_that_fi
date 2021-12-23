from sqlalchemy.orm import Session as sess

from .db_helpers import does_exist
from .db_tracks import does_track_exist, add_track
from .tables import Playlist, Track, PlaylistTracksAssociation
from . import Session 

from src.logger import log

#region create
def add_playlists(playlists: list[dict]):
	with Session.begin() as session:
		for playlist in playlists:
			row = Playlist(playlist)

			if not does_playlist_exist(row.id) and row.owner_id == 'slaybesh':
				log.info(f'Adding playlist: {row.name}')
				session.add(row)
			else:
				log.debug(f'Playlist {row.name} already exists or doesnt belong to you.')


def	add_tracks_to_playlist(playlist_id: str, tracks: list[dict]):
	with Session.begin() as session:
		session: sess = session
		playlist: Playlist = session.query(Playlist).get(playlist_id)
		for track in tracks:

			row = add_track(session, track)
			if row.id is None:
				continue

			try:
				if is_track_in_playlist(session, playlist.id, row.id):
					log.debug(f'{row.name} is already in {playlist.name}')
					continue
			except Exception as e:
				# log.error(row.name)
				continue

			association = PlaylistTracksAssociation(track)
			association.track = row
			association.playlist = playlist
			playlist.tracks.append(association)

			session.add(association)

			log.debug(f'Adding {row.name} to {playlist.name}')
#endregion create


#region read
def get_playlists():
	with Session.begin() as session:
		session: sess = session
		q = session.query(Playlist).all()
		return [playlist.id for playlist in q]


def is_track_in_playlist(session:sess, playlist_id: str, track_id: str):
	try:
		q = session.query(PlaylistTracksAssociation).filter(
				PlaylistTracksAssociation.track_id == track_id,
				PlaylistTracksAssociation.playlist_id == playlist_id)

		return does_exist(q)
	except Exception as e:
		log.error('song already in playlist')
		return True


def does_playlist_exist(playlist_id: str):
	with Session.begin() as session:
		q = session.query(Playlist).filter(Playlist.id == playlist_id)
		return does_exist(q)
#endregion read


#region update
#endregion update


#region delete
#endregion delete

