from src.data_types import TracksType
class Tracks:

	@staticmethod
	def get_names(tracks: list):
		return [track['track']['name'] for track in tracks]
		
	@staticmethod
	def get_ids(tracks: list):
		return [track['track']['id'] for track in tracks]

	@staticmethod
	def get_duration(tracks: list, duration_scale: str='minutes'):
		""" returns duration of tracks \n
				duration scale should be 'seconds', 'minutes' or 'hours' \n
				default is minutes """

		durations_ms: list[int] = [track['track']['duration_ms'] for track in tracks]
		duration = sum(durations_ms) / 1000

		types = {
			'seconds': duration,
			'minutes': duration / 60,
			'hours': duration / (60 * 60)
		}

		return types.get(duration_scale)
