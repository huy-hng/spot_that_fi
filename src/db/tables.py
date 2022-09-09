from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from src.db import Base as TableBase
from src.types.playlists import PlaylistTrackItem, PlaylistType, TrackDict
from src.types.tracks import LikedTrackItem


def parse_time(time: str):
	# TODO: timezones?
	return datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')

class PlaylistAssociation(TableBase):
	__tablename__ = 'playlist_association'

	playlist_id: str = Column(ForeignKey('playlist.id'), primary_key=True)  # type: ignore
	track_id: str = Column(ForeignKey('track.id'), primary_key=True)  # type: ignore
	track: Track = relationship('Track', back_populates='playlists')
	playlist: Playlist = relationship('Playlist', back_populates='tracks')

	added_by: str = Column(String, nullable=False)  # type: ignore
	added_at: datetime = Column(DateTime, nullable=False)  # type: ignore
	# TODO: implement default order of playlist
	order: int = Column(Integer)  # type: ignore

	def __init__(self, track: PlaylistTrackItem):
		self.added_at = parse_time(track.added_at)
		self.added_by = track.added_by['id']


class Playlist(TableBase):
	__tablename__ = 'playlist'

	id: str = Column(String, primary_key=True)  # type: ignore
	name: str = Column(String, nullable=False)  # type: ignore
	total_tracks: int = Column(Integer, nullable=False)  # type: ignore
	public: bool = Column(Boolean, nullable=False)  # type: ignore
	snapshot_id: str = Column(String, nullable=False)  # type: ignore
	owner_id: str = Column(String, nullable=False)  # type: ignore

	tracks: list[PlaylistAssociation] = relationship(
			'PlaylistAssociation', back_populates='playlist')

	def __init__(self, playlist: PlaylistType) -> None:
		self.id = playlist.id
		self.update(playlist)

	def update(self, playlist: PlaylistType) -> None:
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
	liked: bool = Column(Boolean)  # type: ignore
	liked_at: datetime = Column(DateTime)  # type: ignore

	playlists: list[PlaylistAssociation] = relationship(
			'PlaylistAssociation', back_populates='track')

	def __init__(self, track: TrackDict):
		self.id = track.id
		self.name = track.name
		self.duration_ms = track.duration_ms
		self.popularity = track.popularity
		self.is_local = track.is_local

	def update_liked(self, track: LikedTrackItem):
		self.liked = True
		self.liked_at = parse_time(track.added_at)

	def __repr__(self):
		return f'{self.id=}\n{self.name=}\n{self.is_local=}'
