class Tracks:
	def __init__(self, tracks: list):
		self.tracks = tracks

	def add_tracks(self, tracks: list):
		self.tracks += tracks

	@property
	def names(self):
		return self.filter('name')
		
	@property
	def ids(self):
		return self.filter('id')

	@property
	def duration(self):
		""" returns duration of tracks in seconds """

		durations_ms: list[int] = self.filter('duration_ms')
		duration = sum(durations_ms) / 1000
		
		# types = {
		# 	'seconds': duration,
		# 	'minutes': duration / 60,
		# 	'hours': duration / (60 * 60)
		# }

		return duration


	def filter(self, type_: str):
		return [track['track'][type_] for track in self.tracks]

