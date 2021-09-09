import logging
import datetime
import os

folder_path = '../logs'

if not os.path.isdir(folder_path):
	os.mkdir(folder_path)

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
	'%(levelname)7s|%(asctime)s|%(funcName)20s()|line %(lineno)3s|%(message)3s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

def file_handler(folder, log_level):
	if not os.path.isdir(f'{folder_path}/{folder}'):
		os.mkdir(f'{folder_path}/{folder}')

	handler = logging.FileHandler(
							f'{folder_path}/{folder}/' 
							+ datetime.datetime.now().strftime("%Y-%m-%d") 
							+ '.log')
	handler.setLevel(log_level)
	handler.setFormatter(formatter)
	log.addHandler(handler)

file_handler('debug', logging.DEBUG)
file_handler('info', logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)