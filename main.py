import platform
import os
import sys
from time import sleep, strftime
import datetime
import pytz
import subprocess
import settings
import reporting
import database
import connection
import pub_methods
# import multiprocessing # use when multi processing used
import threading
import crawler_proc


operating_system = platform.system()		# clear terminal screen
if(operating_system == 'Linux'):		#
	os.system('clear')			#
elif(operating_system == 'Windows'):		#
	os.system('cls')			#
settings.init()
connection.init()
database.init()
reporting.init()
pub_methods.thread_clear()
pub_methods.subthread_clear()
print("------------------------------------------------------------------------")
print("  ____                _       ____                        _               ")
print(" |  _ \   __ _  _ __ | | __  / ___| _ __  __ _ __      __| |  ___  _ __   ")
print(" | | | | / _` || '__|| |/ / | |    | '__|/ _` |\ \ /\ / /| | / _ \| '__|  ")
print(" | |_| || (_| || |   |   <  | |___ | |  | (_| | \ V  V / | ||  __/| |  ver")
print(" |____/  \__,_||_|   |_|\_\  \____||_|   \__,_|  \_/\_/  |_| \___||_|" + settings.crawler_version)
print("------------------------------------------------------------------------")
print("OS : " + operating_system + " " + platform.release())
print("------------------------------------------------------------------------")

tables_count = database.check_connection()

if tables_count != None:
    print('### DB connection is live.')
else:
    print('!!! ERROR : cannot connect to database.')
    print('!!! Stopping project ...')
    exit()

print('### User Agent records : ' + str(connection._user_agents_count))
print("------------------------------------------------------------------------")

_session = connection.get_tor_session()

if type(_session)==type("this"):
    print('!!! ERROR : , ' + _session)
    print('!!! Stopping project ...')
    exit()

_tor_ip = connection.get_tor_ip()

if _tor_ip[0:5] == 'error':
    print('!!! ERROR : , ' + _tor_ip)
    print('!!! Stopping project ...')
    exit()

_isp_ip = connection.get_isp_ip()

if _isp_ip[0:5] == 'error':
    print('!!! ERROR : , ' + _isp_ip)
    print('!!! Stopping project ...')
    exit()

print('### TOR IP : ' + _tor_ip)
print('### ISP IP : ' + _isp_ip)
print("------------------------------------------------------------------------")
dark_links_timestamp = database.config_get(2)
print('### DarkLinks timestamp : ' + str(dark_links_timestamp))
dark_filters_timestamp = database.config_get(3)
print('### DarkFilters timestamp : ' + str(dark_filters_timestamp))
dark_links = database.dark_links_list()
dark_links_list = [list(elem) for elem in dark_links]
print('### DarkLinks : ' + str(len(dark_links)))
dark_filters = database.dark_filters_list()
print('### DarkFilters : ' + str(len(dark_filters)))
pub_methods.update_filters(dark_filters)
print("------------------------------------------------------------------------")

_index  = 0
_queue = []


while True:
	# do jobs for current item
	now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
	crawl_time = dark_links_list[_index][6].replace(tzinfo=pytz.UTC) + datetime.timedelta(minutes=dark_links_list[_index][5])
	# print(now)
	# print(crawl_time)
	# print('\n')
	if now >= crawl_time:
		# its crawl time do the crawl
		# update timestamp in db
		#print("\r                                                                                         \r"),
		#print("\rCrawling {0}\r".format(dark_links_list[_index][1])),
		print("Crawling {0}".format(dark_links_list[_index][1]))
		dark_links_list[_index][6] = now
		database.dark_links_update_timestamp(dark_links_list[_index][0],now.strftime('%Y-%m-%d %H:%M:%S'))
		# check thread limits (not implemented yet)
		#_threads_count = pub_methods.thread_count()
		printed = False
		while pub_methods.thread_count() >= settings.threads_max_base:
			#print("\r                                                                                         \r"),
			#print("\rwaiting for resource (threading) threads : {0} \r".format(str(pub_methods.thread_count()))),
			if not(printed):
				print("waiting for resource (threading) threads : {0}".format(str(pub_methods.thread_count())))
				printed = True
			sleep(settings.schedule_thread_waiting_delay)

		_thread_identifier = pub_methods.thread_identifier(str(dark_links_list[_index][0]))

		# run crawler module
		# args : id,url,depth
		_params = str(dark_links_list[_index][0]) + ' ' +  str(dark_links_list[_index][1])  + ' ' + str(dark_links_list[_index][2]) + ' ' + str(_thread_identifier)
		# print("start python crawler.py " + _params)
		# print("start python crawler.py " + _params)
		# multithreading
		threading.Thread(target=crawler_proc.crawl, args=(dark_links_list[_index][0], dark_links_list[_index][1],dark_links_list[_index][2],_thread_identifier)).start()
		# multiprocessing
		'''
		_jobs = []
		if __name__ == '__main__':
			print("Starting Process {0}".format(dark_links_list[_index][1]))
			_job = multiprocessing.Process(name=_thread_identifier,target=crawler_proc.crawl2, args=(dark_links_list[_index][0], dark_links_list[_index][1],dark_links_list[_index][2],_thread_identifier))
			_jobs.append(_job)
			_job.start()
		'''
		############################## os.system("start python crawler.py " + _params)
		#print('\n')
		#print("python crawler.py " + _params)
		sleep(settings.schedule_link_crawl)
	else:
		#print("\r                                                                                         \r"),
		#print("\rSkipping {0}\r".format(dark_links_list[_index][1])),
		print("Skipping {0}".format(dark_links_list[_index][1]))
		sleep(settings.schedule_link_skip)
	# darklinks_timestamp check block
	dark_links_timestamp_flap = database.config_get(2)
	if dark_links_timestamp != dark_links_timestamp_flap:
        # its updated
		dark_links_timestamp = dark_links_timestamp_flap
		dark_links = database.dark_links_list()
		dark_links_list = [list(elem) for elem in dark_links]
		#print("\r                                                                                         \r"),
		#print("\rdark links updated...\r"),
		print("dark links updated...")
		sleep(settings.schedule_links_update_delay)
	# darkfilters_timestamp check block
	dark_filters_timestamp_flap = database.config_get(3)
	if dark_filters_timestamp != dark_filters_timestamp_flap:
		# its updated
		dark_filters_timestamp = dark_filters_timestamp_flap
		dark_filters = database.dark_filters_list()
		pub_methods.update_filters(dark_filters)
		sleep(settings.schedule_filters_update_delay)

	if _index == len(dark_links) - 1:
		_index = 0
	else:
		_index += 1
