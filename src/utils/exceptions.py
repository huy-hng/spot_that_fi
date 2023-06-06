class PlaylistNotFoundError(Exception):
	""" this gets raised if a playlist could not be found 
		on spotify or in a database with either name or id """
	# def __init__(self, message, errors):            
	# 	# Call the base class constructor with the parameters it needs
	# 	super().__init__(message)
				
	# 	# Now for your custom code...
	# 	self.errors = errors
