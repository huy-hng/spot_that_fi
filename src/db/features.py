from datetime import datetime, timedelta
from sqlalchemy.orm import Session as sess

from . import Session 
from src.db.tables import Playlist
# from .db_playlists

from src.helpers.logger import log

#region create
def get_latest_tracks_added_to_playlists(days_old=14) -> list[str]:
	""" returns a list with track_ids
			that have been recently added to playlists """

	with Session.begin() as session:
		session: sess = session
		playlists = session.query(Playlist).all()

		latest_tracks = [] # list with track_ids
		oldest_time = datetime.now() - timedelta(days=days_old)
		for playlist in playlists:
			tracks = playlist.playlist_track_association
			for track in tracks:
				if track.added_at > oldest_time:
					latest_tracks.append(track.track.id)

		return latest_tracks


def update_liked_tracks_not_in_playlists(tracks: list[str]):
	""" this function updates the playlist that containes songs
			that are liked, but not in any other playlists
			(except for this one)\n
			tracks is a list with track ids """

