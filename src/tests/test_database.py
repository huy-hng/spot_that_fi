from src.database import db_helpers

def check_track_in_playlist():
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	track_id = '14fIlfcmFPlj4V2IazeJ25'
	# track_id = 'asd14fIlfcmFPlj4V2IazeJ25'
	res = db_helpers.is_track_in_playlist(playlist_id, track_id)
	print(res)

# check_track_in_playlist()