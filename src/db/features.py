from datetime import datetime, timedelta

from src.db.tables import Playlist
from src.helpers.logger import log

from . import create_session


# region create
def get_latest_tracks_added_to_playlists(days_old=14) -> list[str]:
	""" returns a list with track_ids
			that have been recently added to playlists """

	with create_session() as session:
		playlists = session.query(Playlist).all()

		latest_tracks = []  # list with track_ids
		oldest_time = datetime.now() - timedelta(days=days_old)
		for playlist in playlists:
			tracks = playlist.playlist_track_association
			for track in tracks:
				if track.added_at > oldest_time:
					latest_tracks.append(track.track.id)

		return latest_tracks
