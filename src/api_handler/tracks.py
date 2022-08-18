from enum import Enum
from src.helpers.data_types import TracksType

class DurationScale(Enum):
	SECONDS = 'seconds'
	MINUTES = 'minutes'
	HOURS = 'hours'

class Tracks:

	@staticmethod
	def get_names(tracks: list[dict]):
		return [track['track']['name'] for track in tracks]
		
	@staticmethod
	def get_ids(tracks: list[dict]):
		return [track['track']['id'] for track in tracks]

	@staticmethod
	def get_duration(tracks: list[dict], duration_scale: DurationScale):
		""" returns duration of tracks \n
				duration scale should be 'seconds', 'minutes' or 'hours' \n
				default is minutes """

		durations_ms: list[int] = [track['track']['duration_ms'] for track in tracks]
		duration = sum(durations_ms) / 1000

		types = {
			DurationScale.SECONDS: duration,
			DurationScale.MINUTES: duration / 60,
			DurationScale.HOURS: duration / (60 * 60)
		}

		return types[duration_scale]
