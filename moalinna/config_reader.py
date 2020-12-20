import configparser
import os

found_files = []

def open_config_file(BASE_DIR):
	global found_files

	config_search_order = [
		os.getenv('MOALINNA_SETTINGS_FILE'),
		os.path.join(BASE_DIR, 'settings_dev.ini'),
		os.path.join(os.path.expandvars('$APPDATA'), 'moalinna/settings.ini'),
		'/etc/moalinna/settings.ini',
	]

	config = configparser.ConfigParser()
	found_files = config.read((fn for fn in config_search_order if fn), encoding='utf-8')
	if not found_files:
		raise IOError("No configuration file found.")
	return config
