from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from src.types.playlists import AllPlaylists, PlaylistTracksItem, SinglePlaylist
from src.types.tracks import TrackDict


from src.db import Base as TableBase


class PlaylistTracksAssociation(TableBase):
	__tablename__ = 'playlist_tracks_association'

	playlist_id: str = Column(
		ForeignKey('playlist.id'), primary_key=True)  # type: ignore
	track_id: str = Column(
		ForeignKey('track.id'), primary_key=True)  # type: ignore
	track: Track = relationship('Track',
			back_populates='playlist_track_association')
	playlist: Playlist = relationship('Playlist',
			back_populates='playlist_track_association')

	added_by: str = Column(String, nullable=False)  # type: ignore
	added_at: datetime = Column(DateTime, nullable=False)  # type: ignore

	def __init__(self, track: PlaylistTracksItem):
		self.added_at = datetime.strptime(track.added_at, '%Y-%m-%dT%H:%M:%SZ')
		self.added_by = track.added_by['id']


class Playlist(TableBase):
	__tablename__ = 'playlist'

	id: str = Column(String, primary_key=True)  # type: ignore
	name: str = Column(String, nullable=False)  # type: ignore
	total_tracks: int = Column(Integer, nullable=False)  # type: ignore
	public: bool = Column(Boolean, nullable=False)  # type: ignore
	snapshot_id: str = Column(String, nullable=False)  # type: ignore
	owner_id: str = Column(String, nullable=False)  # type: ignore

	playlist_track_association: list[PlaylistTracksAssociation] = relationship(
			'PlaylistTracksAssociation', back_populates='playlist')

	def __init__(self, playlist: AllPlaylists | SinglePlaylist) -> None:
		self.id = playlist.id
		self.update(playlist)

	def update(self, playlist: AllPlaylists | SinglePlaylist) -> None:
		self.name = playlist.name
		self.total_tracks = playlist.tracks.total
		self.public = playlist.public
		self.snapshot_id = playlist.snapshot_id
		self.owner_id = playlist.owner.id


class Track(TableBase):
	__tablename__ = 'track'

	id: str = Column(String, primary_key=True)  # type: ignore
	name: str = Column(String, nullable=False)  # type: ignore
	duration_ms: int = Column(Integer, nullable=False)  # type: ignore
	popularity: int = Column(Integer, nullable=False)  # type: ignore
	liked: bool = Column(Boolean, default=False)  # type: ignore

	playlist_track_association: list[PlaylistTracksAssociation] = relationship(
			'PlaylistTracksAssociation', back_populates='track')

	def __init__(self, track: TrackDict):
		self.id = track.id
		self.name = track.name
		self.duration_ms = track.duration_ms
		self.popularity = track.popularity
		self.is_local = track.is_local

	def __repr__(self):
		return f'{self.id=}\n{self.name=}\n{self.is_local=}'
