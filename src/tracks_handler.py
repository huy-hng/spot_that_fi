class Tracks:
	def __init__(self, tracks: list):
		self.tracks = tracks

	@property
	def names(self):
		return self.filter('name')
		
	@property
	def ids(self):
		return self.filter('id')

	def filter(self, type_: str):
		return [track['track'][type_] for track in self.tracks]
