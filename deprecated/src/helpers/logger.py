import logging
import datetime
import os

folder_path = './logs'

if not os.path.isdir(folder_path):
	os.mkdir(folder_path)

log = logging.getLogger('My Logger')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
	'%(levelname)7s|%(asctime)s|%(funcName)20s()|line %(lineno)3s|%(message)3s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

console_formatter = logging.Formatter('%(message)3s')


def add_file_handler(level, log_level):
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	path = f'{folder_path}/{date}'

	if not os.path.isdir(path):
		os.mkdir(path)

	handler = logging.FileHandler(f'{path}/{level}.log')
	handler.setLevel(log_level)
	handler.setFormatter(formatter)
	log.addHandler(handler)

add_file_handler('debug', logging.DEBUG)
add_file_handler('info', logging.INFO)
add_file_handler('error', logging.ERROR)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(console_formatter)
consoleHandler.setLevel(logging.INFO)
log.addHandler(consoleHandler)
