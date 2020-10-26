import platform
import os
import sys
from bs4 import BeautifulSoup
from PyCRC.CRC32 import CRC32
from time import sleep, strftime
import datetime
import pytz
import unicodedata
import re
import settings
import reporting
import database
import connection
import pub_methods

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
    # handling input parameters
    params = sys.argv[1:]
    if len(params) > 5 or len(params) < 4:
        print('!!! ERROR : invalid parameters.')
        print('!!! Stopping project ...')
        exit()
    _subcrawler_flag = False
    config_crawl_parent = ''
    if len(params) == 5:
        _subcrawler_flag = True
        config_crawl_parent = params[4]
    else:
        config_crawl_parent = params[0]
    config_crawl_id = params[0]
    config_crawl_url = params[1]
    config_crawl_depth = int(params[2])
    config_crawl_identifier = params[3]
    # detecting operating system
    operating_system = platform.system()		# clear terminal screen
    if(operating_system == 'Linux'):		#
    	os.system('clear')			#
    elif(operating_system == 'Windows'):		#
    	os.system('cls')			#
    # initialing modules
    settings.init()
    connection.init()
    database.init()
    reporting.init()
    print('                                                       ')
    print(' _____               _         _____         _         ')
    print('|     |___ ___ _ _ _| |___ ___|   __|___ ___|_|___ ___ ')
    print("|   --|  _| .'| | | | | -_|  _|   __|   | . | |   | -_|")
    print('|_____|_| |__,|_____|_|___|_| |_____|_|_|_  |_|_|_|___|')
    print('                                        |___|     ' + settings.crawler_engine_version)
    print("------------------------------------------------------------------------")
    print("OS : " + operating_system + " " + platform.release())
    print("------------------------------------------------------------------------")
    tables_count = database.check_connection()
    if tables_count != None:
        print('### DB connection is live.')
    else:
        print('!!! ERROR : cannot connect to database.')
        print('!!! Stopping project ...')
        if _subcrawler_flag:
            pub_methods.subthread_remove(config_crawl_identifier)
        else:
            pub_methods.thread_remove(config_crawl_identifier)
        exit()
    print('### User Agent records : ' + str(connection._user_agents_count))
    print("------------------------------------------------------------------------")
    _session = connection.get_tor_session()
    if type(_session)==type("this"):
        print('!!! ERROR : , ' + _session)
        print('!!! Stopping project ...')
        if _subcrawler_flag:
            pub_methods.subthread_remove(config_crawl_identifier)
        else:
            pub_methods.thread_remove(config_crawl_identifier)
        exit()
    if settings.crawler_engine_ipcheck:
        _tor_ip = connection.get_tor_ip()
        if _tor_ip[0:5] == 'error':
            print('!!! ERROR : , ' + _tor_ip)
            print('!!! Stopping project ...')
            if _subcrawler_flag:
                pub_methods.subthread_remove(config_crawl_identifier)
            else:
                pub_methods.thread_remove(config_crawl_identifier)
            exit()
        print('### TOR IP : ' + _tor_ip)
        _isp_ip = connection.get_isp_ip()
        if _isp_ip[0:5] == 'error':
            print('!!! ERROR : , ' + _isp_ip)
            print('!!! Stopping project ...')
            if _subcrawler_flag:
                pub_methods.subthread_remove(config_crawl_identifier)
            else:
                pub_methods.thread_remove(config_crawl_identifier)
            exit()
        print('### ISP IP : ' + _isp_ip)
    print("------------------------------------------------------------------------")
    # load filters
    _filters = pub_methods.load_filters()
    if _filters == None:
        print('!!! ERROR : , cannot load filters.')
        print('!!! Stopping project ...')
        if _subcrawler_flag:
            pub_methods.subthread_remove(config_crawl_identifier)
        else:
            pub_methods.thread_remove(config_crawl_identifier)
        exit()
    print('### Filters loaded : ' + str(len(_filters)))
    # load url full required details of dark link
    _dark_link = ''
    if _subcrawler_flag:
        print('### SUBCRAWLER ###')
    else:
        _dark_link = database.dark_links_data(config_crawl_id)
        if _dark_link == None:
            print('!!! ERROR : , cannot get dark link record in database')
            print('!!! Stopping project ...')
            if _subcrawler_flag:
                pub_methods.subthread_remove(config_crawl_identifier)
            else:
                pub_methods.thread_remove(config_crawl_identifier)
            exit()

        if len(_dark_link) == 0:
            print('!!! ERROR : , cannot find dark link record in database..')
            print('!!! Stopping project ...')
            if _subcrawler_flag:
                pub_methods.subthread_remove(config_crawl_identifier)
            else:
                pub_methods.thread_remove(config_crawl_identifier)
            exit()
    # load pattern based rules if link navigation is allowed (depth > 0)
    _dark_link_subdata = ''
    if _subcrawler_flag:
        #if config_crawl_depth >= 0:
        _dark_link_subdata = database.dark_links_subdata(config_crawl_parent)
        if _dark_link_subdata == None:
            print('!!! ERROR : , cannot get dark link pattern based rules from database')
            print('!!! Stopping project ...')
            if _subcrawler_flag:
                pub_methods.subthread_remove(config_crawl_identifier)
            else:
                pub_methods.thread_remove(config_crawl_identifier)
            exit()
    _content = pub_methods.get_onion_content(config_crawl_url,_session)
    if _content == None:
        print('!!! ERROR : , cannot get onion content..')
        print('!!! Stopping project ...')
        if _subcrawler_flag:
            pub_methods.subthread_remove(config_crawl_identifier)
        else:
            pub_methods.thread_remove(config_crawl_identifier)
        exit()
    _subcrawler_rules = []
    _subcrawler_rules_count = 0
    if _subcrawler_flag:
        if _dark_link_subdata != None:
            for _item in _dark_link_subdata:
                try:
                    _pattern = re.compile(_item[1])
                    _res = _pattern.search(config_crawl_url,re.I)
                    if _res:
                        #_res = re.find(_pattern, config_crawl_url)
                        _subcrawler_rules.append([_item[2],_item[3]])
                        _subcrawler_rules_count += 1
                except Exception as e:
                    reporting.report('warning', 'medium', 'crawler.py > ERRX01 (subcrawler regex detection)',str(e))
                    print(str(e))
    _parsed_content = BeautifulSoup(_content,'html.parser')
    _page_title = '-'
    if _parsed_content.title != None:
        _page_title = str(_parsed_content.title.string)
    print(">>> Title : " + _page_title)
    _links = _parsed_content.find_all('a')
    print(">>> Links count : " + str(len(_links)))
    print('### Session : ' + config_crawl_identifier)
    _filtered_content = ''
    if _subcrawler_flag:
        for _rule in _subcrawler_rules:
            if _rule[0] != None:
                for _tag in _parsed_content.select(_rule[0]):
                    #_filtered_content += _tag
                    _filtered_content += str(_tag)
                _filtered_content = BeautifulSoup(_filtered_content,'html.parser')
                if _rule[1] != None:
                    print('>>> Target blocks : Only allowed blocks except rejected items will be crawled.')
                    for _tag in _filtered_content.select(_dark_link[0][4]):
                        _tag.decompose()
                else:
                    print('>>> Target blocks : Only allowed blocks will be crawled.')
            else:
                if _rule[1] != None:
                    print('>>> Target blocks : All blocks except rejected items will be crawled.')
                    for _tag in _parsed_content.select(_rule[1]):
                        _tag.decompose()
                    _filtered_content = _parsed_content
                else:
                    print('>>> Target blocks : All blocks will be crawled.')
                    _filtered_content = _parsed_content
            # not implemented yet :
            """ it has to combine rules detected
                it's not implemented yet but it has to """
        if len(_subcrawler_rules) == 0:
            _filtered_content = _parsed_content
    else:
        if _dark_link[0][3] != None:
            for _tag in _parsed_content.select(_dark_link[0][3]):
                #_filtered_content += _tag
                _filtered_content += str(_tag)
            _filtered_content = BeautifulSoup(_filtered_content,'html.parser')
            if _dark_link[0][4] != None:
                print('>>> Target blocks : Only allowed blocks except rejected items will be crawled.')
                for _tag in _filtered_content.select(_dark_link[0][4]):
                    _tag.decompose()
            else:
                print('>>> Target blocks : Only allowed blocks will be crawled.')
            #print(_filtered_content)
        else:
            if _dark_link[0][4] != None:
                print('>>> Target blocks : All blocks except rejected items will be crawled.')
                for _tag in _parsed_content.select(_dark_link[0][4]):
                    _tag.decompose()
                _filtered_content = _parsed_content
            else:
                print('>>> Target blocks : All blocks will be crawled.')
                _filtered_content = _parsed_content
    print('>>> Matched elements by rules : ' + str(len(_filtered_content)))
    if _subcrawler_flag:
        print(_subcrawler_rules)
        #print(str(_filtered_content.get_text().replace(u'\xe2','')))
    final_text =  str(_filtered_content.get_text()).replace(u'\xe2','')
    #final_text = final_text.encode('utf-8', 'ignore').decode('utf-8')
    _checksum = CRC32().calculate(str(final_text))
    print(">>> CRC32 checksum : " + str(_checksum))
    if _subcrawler_flag:
        # get page last _checksum
        _dataX = database.dark_links_url_hash(config_crawl_id,config_crawl_url)
        ##print(_dataX)
        if _dataX == None:
            # its first time for a while crawling add current checksum to table
            _now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            database.dark_links_url_hash_insert(config_crawl_id,config_crawl_url,_now.strftime('%Y-%m-%d %H:%M:%S'),_checksum)
        else:
            if len(_dataX) > 0:
                if str(_dataX[0][3]) == str(_checksum):
                    print(">>> Updates : No Difference found.")
                    print('>>> Data control skipped ...')
                    if _subcrawler_flag:
                        pub_methods.subthread_remove(config_crawl_identifier)
                    else:
                        pub_methods.thread_remove(config_crawl_identifier)
                    exit()
                else:
                    print(">>> Updates : Page updated.")
                    database.dark_links_url_hash_update(config_crawl_id,config_crawl_url,_checksum)
            else:
                _now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
                database.dark_links_url_hash_insert(config_crawl_id,config_crawl_url,_now.strftime('%Y-%m-%d %H:%M:%S'),_checksum)
    else:
        if str(_checksum) == str(_dark_link[0][7]):
            print(">>> Updates : No Difference found.")
            print('>>> Data control skipped ...')
            if _subcrawler_flag:
                pub_methods.subthread_remove(config_crawl_identifier)
            else:
                pub_methods.thread_remove(config_crawl_identifier)
            exit()
        else:
            print(">>> Updates : Page updated.")
            database.dark_links_update_checksum(_dark_link[0][0],_checksum)
    #print(final_text)
    _final_text = _filtered_content.get_text()
    _i_index = 0
    _matched_filters = []
    _content_priority = 0
    print('##### FINAL TEXT LENGTH : ' + str(len(_final_text)))
    for _filter in _filters:
        try:
            _single_matched = False
            _pattern = re.compile(_filter[1])
            #print('!!! filter check {' +  str(_filter[1]) + "}")
            if _filter[6] != None:
                # hybrid filter
                # not implemented yet :
                """ it has to detect hybrid filters
                    it's not implemented yet but it has to """
                _res = _pattern.search(_final_text,re.I)
                if _res:
                    #_res = re.find(_pattern, config_crawl_url)
                    _single_matched = True
                    _j_index = _i_index + 1
                    #for j in range(_j_index, len(_filters)):
            else:
                # single filter
                _res = _pattern.search(_final_text,re.I)
                if _res:
                    #_res = re.find(_pattern, config_crawl_url)
                    _single_matched = True
                    print('!!! filter matched {' +  str(_filter[0]) + "}")
                    _matched_filters.append([_filter[0],str(_filter[1])])
                    _content_priority += int(_filter[4])
        except Exception as e:
            reporting.report('warning', 'medium', 'crawler.py > ERRX02 (data analysis)',str(e))
            print(str(e))
    print('##### MATCHED FILTERS COUNT : ' + str(len(_matched_filters)))
    if len(_matched_filters) > 0:
        # generate ID for content
        _now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        _temp_id = pub_methods.generate_hash(config_crawl_url + '_' + _now.strftime('%Y-%m-%d %H:%M:%S %f'))
        _content_key = pub_methods.generate_hash(_temp_id)
        _seen = ''
        for _m in _matched_filters:
            if len(_seen) > 0:
                _seen += '~'
            _seen += _m[1]
        _r1 = database.content_new(_temp_id,config_crawl_url,"DARK-TOR","DARK-TOR",_seen,_content_priority,_now.strftime('%Y-%m-%d %H:%M:%S'))
        _r2 = database.content_data(_temp_id,_final_text)
        for _f in _matched_filters:
            _r3 = database.content_filter(_temp_id,_f[0])
        for _x in range(1,8):
            database.content_user(_temp_id,str(_x))
        print('##### REPORT INSERTED, ID : ' + str(_temp_id))
    print('>>> Depth : ' + str(config_crawl_depth))
    if config_crawl_depth > 0:
        # links and url navigation
        _links = _filtered_content.find_all('a')
        _links_count = 0
        _links_list = []
        for _link in _links:
            if _link['href'] != None:
                _onion_index = str(_link['href']).find('.onion')
                _http_index = str(_link['href']).find('http://')
                _https_index = str(_link['href']).find('https://')
                _current_domain = config_crawl_url[:config_crawl_url.find('.onion')]
                _current_domain = _current_domain.replace('http://','')
                _current_domain = 'http://' + _current_domain + '.onion'
                if _onion_index == -1:
                    # it has not .onion and it's local for domain
                    if _http_index != -1 or _https_index != -1:
                        # it is not local for current domain it has http
                        _link.decompose()
                    else:
                        # it is local for current domain
                        _final_link = ''
                        if str(_link['href']).startswith('/'):
                            _final_link = _current_domain + str(_link['href'])
                        else:
                            _final_link = _current_domain + '/' + str(_link['href'])
                        _links_list.append(_final_link)
                        _links_count += 1
                else:
                    # it has .onion and it can be both of internal and external
                    _domain = (str(_link['href'])[:_onion_index]).replace('http://','')

                    if 'http://' + _domain == _current_domain:
                        # its local
                        _links_list.append('http://' + _domain)
                        _links_count += 1
                    else:
                        # its not local link, so skip
                        _link.decompose()
        # continue
        print(">>> Confirmed urls for crawl proccess : " + str(len(_links_list)))
        #print(_links_list)
        for _link in _links_list:
            while pub_methods.subthread_count() >= settings.threads_max_sub:
            	print("\r                                                                                         \r"),
            	print("\rwaiting for resource (threading) threads : {0} \r".format(str(pub_methods.subthread_count()))),
            	sleep(settings.schedule_subthread_waiting_delay)
            _thread_identifier = pub_methods.subthread_identifier(str(config_crawl_id),_link)
            _subthread_parent = ''
            # run crawler module
            # args : id,url,depth
            _params = str(config_crawl_id) + ' ' + str(_link)  + ' ' + str(config_crawl_depth - 1) + ' ' + str(_thread_identifier) + ' ' + str(config_crawl_id)
            # print("start python crawler.py " + _params)
            os.system("start python crawler.py " + _params)
            #print('\n')
            #print("start python crawler.py " + _params)
            #print('\n')
            sleep(settings.schedule_sublink_crawl)
except Exception as e:
    reporting.report('Error','Critical','crawler > final try',str(e))
    print('!!!!!!!!! CRASHED !!!!!!!!!')
if _subcrawler_flag:
    pub_methods.subthread_remove(config_crawl_identifier)
else:
    pub_methods.thread_remove(config_crawl_identifier)
#_oio = input()
sleep(10)
