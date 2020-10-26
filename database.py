#
##
### USED PUBLIC MODULES
##
#
import mysql.connector
#
##
### CRAWLER MODULES
##
#
import settings
import reporting
#
##
### INITIAL METHOD
##
#

def init(_log=True):
	try:
		global db_connection
		#db_connection = MySQLdb.connect(host=settings.db_host,						# db host, usually localhost
		#			     				user=settings.db_user,						# db user account username
		#			     				passwd=settings.db_pass,					# db user account password
		#			     				db=settings.db_name)						# name of the database
		db_connection = mysql.connector.connect(host=settings.db_host,
												user=settings.db_user,
												passwd=settings.db_pass,
												database=settings.db_name,
												autocommit=True)
		if _log:
			print("### Database module is online...")
	except Exception as e:
		reporting.report('error', 'critical', 'database module > init', str(e))

def check_connection():
	try:
		mycur = db_connection.cursor()
		xx = mycur.execute("show tables")
		table_count = 0
		for table in mycur:
			table_count+=1
		return table_count
	except Exception as e:
		reporting.report('error', 'critical', 'database module > check_connection', str(e))
		return None

""" CONFIG methods """

def config_get(id):
	try:
		mycur = db_connection.cursor()
		mycur.execute("select `value` from `config` where `id` = " + str(id) + ";")
		myresult = mycur.fetchall()
		return myresult[0][0]
	except Exception as e:
		reporting.report('error', 'critical', 'database module > config_get', str(e))
		return None

def config_set(id, value):
	try:
		mycur = db_connection.cursor()
		mycur.execute("update `config` set `value` = '" + value + "' where `id` = " + str(id) + ";")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > config_set', str(e))
		return None

""" DARK_LINKS methods """

def dark_links_list():
	try:
		mycur = db_connection.cursor()
		mycur.execute("select * from `dark_links` order by `crawl_last` ASC;")
		myresult = mycur.fetchall()
		return myresult
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_list', str(e))
		return None

def dark_links_update_timestamp(id, timestamp):
	try:
		mycur = db_connection.cursor()
		mycur.execute("update `dark_links` SET `crawl_last` = '"+ timestamp +"' WHERE `id` = "+str(id)+";")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_update_timestamp', str(e))
		return None

def dark_links_update_checksum(id, checksum):
	try:
		mycur = db_connection.cursor()
		mycur.execute("update `dark_links` SET `checksum` = '"+ str(checksum) +"' WHERE `id` = "+str(id)+";")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_update_checksum', str(e))
		return None

def dark_links_data(_id):
	try:
		mycur = db_connection.cursor()
		mycur.execute("select * from `dark_links` WHERE `id` = " + _id + ";")
		myresult = mycur.fetchall()
		return myresult
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_data', str(e))
		return None

def dark_links_url_hash(_id, _url):
	try:
		mycur = db_connection.cursor()
		mycur.execute("select * from `dark_links_checksum` WHERE `id` = " + str(_id) + " AND `url` = '"+ str(_url) + "';")
		myresult = mycur.fetchall()
		return myresult
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_url_hash', str(e))
		return None

def dark_links_url_hash_insert(_id, _url, _time, _hash):
	try:
		mycur = db_connection.cursor()

		mycur.execute("insert into `dark_links_checksum` (`id`,`url`,`crawl_last`,`checksum`) values ("+str(_id)+",'" + _url + "','" + _time + "','" + str(_hash) + "');")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_url_hash_insert', str(e))
		return None

def dark_links_url_hash_update(_id, _url, _hash):
	try:
		mycur = db_connection.cursor()
		mycur.execute("update `dark_links_checksum` SET `checksum` = '"+ str(_hash) +"' WHERE `id` = "+str(_id)+" AND `url` = '" + _url + "';")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_url_hash_update', str(e))
		return None

def dark_links_subdata(_id):
	try:
		mycur = db_connection.cursor()
		mycur.execute("select * from `dark_link_rules` WHERE `id` = " + _id + ";")
		myresult = mycur.fetchall()
		return myresult
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_links_subdata', str(e))
		return None

""" DARK_FILTERS methods """

def dark_filters_list():
	try:
		mycur = db_connection.cursor()
		mycur.execute("select * from `filters` WHERE `platform` = 'dark_tor' order by `group` ASC;")
		myresult = mycur.fetchall()
		return myresult
	except Exception as e:
		reporting.report('error', 'critical', 'database module > dark_filters_list', str(e))
		return None

""" CONTENTS methods """

def content_new(_key,_title,_syntax,_user,_seen,_priority,_date):
	try:
		mycur = db_connection.cursor()
		mycur.execute("insert into `pastes` (`key`,`title`,`syntax`,`user`,`important`,`catched`,`seen`,`platform`,`priority`,`date_paste`,`date_crawl`) values ('"+_key+"','"+_title+"','"+_syntax+"','"+_user+"',b'1',b'1','"+_seen+"','pb',"+str(_priority)+",'"+_date+"','"+_date+"');")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > content_new', str(e))
		return None

def content_data(_key,_data):
	try:
		mycur = db_connection.cursor()
		mycur.execute("insert into `pastes_data` (`key`,`data`) values (%s,%s);",(_key,_data))
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > content_data', str(e))
		return None

def content_filter(_key,_filterid):
	try:
		mycur = db_connection.cursor()
		mycur.execute("insert into `pastes_filters` (`key`,`filter_id`) values ('"+_key+"',"+str(_filterid)+");")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > content_filter', str(e))
		return None
def content_user(_key,_userid):
	try:
		mycur = db_connection.cursor()
		mycur.execute("insert into `pastes_users` (`key`,`user`) values ('"+_key+"',"+str(_userid)+");")
		db_connection.commit()
		return mycur.rowcount
	except Exception as e:
		reporting.report('error', 'critical', 'database module > content_user', str(e))
		return None
