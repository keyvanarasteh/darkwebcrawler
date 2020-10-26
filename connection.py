import requests
import random
import json
import settings
import reporting

def init(_log=True):
    global _user_agent, _user_agents_count

    #f = open('assets/user-agents.dat')
    #_user_agents = f.read()
    #content = _user_agents.split('\n')
    with open('assets/user-agents.dat') as f:
		content = f.read().splitlines()
    _user_agents_count = len(content)
    _user_agent = content[random.randint(0,len(content))]
    if _log:
        print("### Connection module is online...")

def get_tor_session():
    try:
        global session
    	session = requests.session()
    	# Tor uses the 9050 port as the default socks port
    	session.proxies = settings.proxy_config
    	# Set Random User Agent for request
    	# lines = tuple(open('assets/user-agents.dat','r'))
        if settings._update_user_agent:
    	       session.headers.update({'user-agent':_user_agent})
    	return session
    except Exception as e:
        reporting.report('error', 'critical', 'connection module > get_tor_session', str(e))
    	return 'error : ' + str(e)


def get_tor_ip():
    try:
    	# this should get an IP different than your public IP
    	ip_info = json.loads(session.get("http://httpbin.org/ip").text);
    	# this should print an IP different than your public IP
    	return ip_info['origin']
    except Exception as e:
        reporting.report('error', 'important', 'connection module > get_tor_ip', str(e))
    	return 'error : ' + str(e)

def get_isp_ip():
    try:
    	# this should get your ISP public IP
    	ip_info = json.loads(requests.get("http://httpbin.org/ip").text);
    	# this should print your ISP public IP
    	return ip_info['origin']
    except Exception as e:
    	reporting.report('error', 'important', 'connection module > get_isp_ip', str(e))
    	return 'error : ' + str(e)
