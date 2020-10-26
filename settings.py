# settings.py
def init(_log=True):
	# base variables
	global crawler_version, db_host, db_user, db_pass, db_name
	global proxy_config
	#''' # DEBUG:
	db_host = 'localhost'
	db_user = ''
	db_pass = ''
	db_name = ''
	crawler_version = '2.0.1'
	#'''
	''' # SERVER
	db_host = 'localhost'
	db_user = ''
	db_pass = '' 
	db_name = '' 
	crawler_version = '2.0.1'
	'''
	proxy_config = {'http' : 'socks5h://127.0.0.1:9050',
					'https': 'socks5h://127.0.0.1:9050'}
	# crawler engine variables
	global crawler_engine_version, crawler_engine_ipcheck
	crawler_engine_version = '1.0.3'
	crawler_engine_ipcheck = False
	# timer variables
	global schedule_link_skip, schedule_link_crawl, schedule_sublink_crawl, schedule_links_update_delay, schedule_filters_update_delay, schedule_thread_waiting_delay, schedule_subthread_waiting_delay
	schedule_link_skip = 0.1
	schedule_link_crawl = 1
	schedule_sublink_crawl = 1
	schedule_links_update_delay = 1
	schedule_filters_update_delay = 1
	schedule_thread_waiting_delay = 0.5
	schedule_subthread_waiting_delay = 0.5
	# threading variables
	global threads_max_base, threads_max_sub
	threads_max_base = 2
	threads_max_sub = 1
	global _update_user_agent
	_update_user_agent = True
	if _log:
		print('### Config module is online.')
