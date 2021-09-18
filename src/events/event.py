from typing import Callable

class EventHandler:
	subscribers: dict[str, list[Callable]] = dict()

	def subscribe(self, event_type: str, fn: Callable):
		if not event_type in self.subscribers:
			self.subscribers[event_type] = []
		self.subscribers[event_type].append(fn)

	def post(self, event_type: str, data): # TODO data could be kwargs
		if not event_type in self.subscribers:
			raise ValueError(f'Event {event_type} does not exist.')
		for fn in self.subscribers[event_type]:
			fn(data)
