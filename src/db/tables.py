from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from src.types.playlists import SpotifyPlaylistType

from src.db import Base as TableBase

class PlaylistTracksAssociation(TableBase):
	__tablename__ = 'playlist_tracks_association'

	playlist_id = Column(ForeignKey('playlist.id'), primary_key=True)
	track_id = Column(ForeignKey('track.id'), primary_key=True)
	track: Track = relationship('Track',
										back_populates='playlist_track_association')
	playlist: Playlist = relationship('Playlist',
													back_populates='playlist_track_association')

	added_by = Column(String, nullable=False)
	added_at = Column(DateTime, nullable=False)

	def __init__(self, track):
		self.added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
		self.added_by = track['added_by']['id']


class Playlist(TableBase):
	__tablename__ = 'playlist'

	id = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	total_tracks = Column(Integer, nullable=False)
	public = Column(Boolean, nullable=False)
	snapshot_id = Column(String, nullable=False)
	owner_id = Column(String, nullable=False)

	playlist_track_association: list[PlaylistTracksAssociation] = relationship(
			'PlaylistTracksAssociation', back_populates='playlist')

	def __init__(self, playlist: SpotifyPlaylistType) -> None:
		self.id = playlist.id
		self.update(playlist)

	def update(self, playlist: SpotifyPlaylistType) -> None:
		self.name = playlist.name
		self.total_tracks = playlist.tracks.total
		self.public = playlist.public
		self.snapshot_id = playlist.snapshot_id
		self.owner_id = playlist.owner.id


class Track(TableBase):
	__tablename__ = 'track'

	id = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	duration_ms = Column(Integer, nullable=False)
	popularity = Column(Integer, nullable=False)
	liked = Column(Boolean, default=False)

	playlist_track_association: list[PlaylistTracksAssociation] = relationship(
			'PlaylistTracksAssociation', back_populates='track')

	def __init__(self, track: dict):
		self.id = track['track']['id']
		self.name = track['track']['name']
		self.duration_ms = track['track']['duration_ms']
		self.popularity = track['track']['popularity']
		self.is_local = track['is_local']

	def __repr__(self):
		return f'{self.id=}\n{self.name=}\n{self.is_local=}'
