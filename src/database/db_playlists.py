from sqlalchemy.orm import Session as sess

from .db_helpers import does_exist
from .db_tracks import add_track
from .tables import Playlist, PlaylistTracksAssociation
from . import Session 

from src.helpers.logger import log

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
			if row is None or row.id is None:
				continue

			try:
				if is_track_in_playlist(session, playlist.id, row.id):
					log.debug(f'{row.name} is already in {playlist.name}')
					continue
			except Exception as e:
				log.exception(e) # TODO find out what this error is
				log.error(f'Not sure what this error is.')
				continue

			association = PlaylistTracksAssociation(track)
			association.track = row
			association.playlist = playlist
			playlist.playlist_track_association.append(association)

			session.add(association)

			log.debug(f'Adding {row.name} to {playlist.name}')
#endregion create


#region read
def get_playlist_tracks(session: sess, playlist_name: str):
	playlist = session.query(Playlist).filter(Playlist.name == playlist_name).first()
	return playlist.playlist_track_association



def get_playlists():
	with Session.begin() as session:
		session: sess = session
		q = session.query(Playlist).all()
		return [playlist.id for playlist in q]


def is_track_in_playlist(session:sess, playlist_id: str, track_id: str):
	q = session.query(PlaylistTracksAssociation).filter(
										PlaylistTracksAssociation.track_id == track_id,
										PlaylistTracksAssociation.playlist_id == playlist_id)
	return does_exist(q)


def does_playlist_exist(playlist_id: str):
	with Session.begin() as session:
		q = session.query(Playlist).get(playlist_id)
		if q is None:
			return False
		return True
#endregion read


#region update
def update_liked_tracks_not_in_playlists(tracks: list[str]):
	""" this function updates the playlist that containes songs
			that are liked, but not in any other playlists
			(except for this one)\n
			tracks is a list with track ids """

#endregion update


#region delete
#endregion delete

