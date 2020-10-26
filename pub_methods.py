import os
import json
import reporting
import requests
import hashlib

def update_filters(filters):
	# create working flag
    try:
    	if os.path.exists('temp/working.flag'):
            os.remove('temp/working.flag')
        working_flag = open('temp/working.flag','w+')
        working_flag.write('x')
        working_flag.close()
    	# open output file for writing
    	filehandle = open('temp/filters.dat','w+')
    	json.dump(filters,filehandle)
    	if os.path.exists('temp/working.flag'):
    		os.remove('temp/working.flag')

        print("\r                                                                 \r"),
    	print("\rfilters updated...\r"),
    except Exception as e:
        reporting.report('error', 'critical', 'pub_methods module > update_filters', str(e))
        return None

def load_filters():
    try:
        # wait if base engine is updating filters from Database
        _stop_flag = True
        while _stop_flag:
            if(os.path.exists('temp/working.flag')):
                sleep(0.5)
            else:
                _stop_flag = False
        # load filters from file
        if os.path.exists('temp/filters.dat'):
            _filters = ''
            with open('temp/filters.dat','r') as f:
                _filters = json.load(f)

            return _filters;
        else:
            reporting.report('error', 'critical', 'pub_methods module > load_filters (X01)', str(e))
            return None


    except Exception as e:
        reporting.report('error', 'critical', 'pub_methods module > load_filters (X02)', str(e))
        return None

def get_onion_content(url, session):
    try:
        _content = session.get(url, verify=False).text
        print("Content URL : " + url)
        print("Content length : " + str(len(_content)))
        print("------------------------------------------------------------------------")
        return _content
    except Exception,e:
        reporting.report('error', 'critical', 'crawler > get_onion_content', str(e))
        return None

def generate_hash(_input):
    m = hashlib.md5()
    m.update(_input)
    return str(m.hexdigest())

def thread_count():
    _dirs = os.listdir('threads')
    return len(_dirs)

def thread_remove(identifier):
    if os.path.exists('threads/' + identifier):
        os.unlink('threads/' + identifier)

def thread_clear():
    folder = 'threads'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def thread_identifier(_h='x'):
    _index = 01
    _base = 'thread_' + _h + '_'
    for i in range(1,500):
        _file = _base + str(_index) + '.session'
        if os.path.exists('threads/' + _file):
            _index += 1
            continue
        else:
            f = open('threads/' + _file,'w+')
            return _file

def subthread_count():
    _dirs = os.listdir('threads_sub')
    return len(_dirs)

def subthread_remove(identifier):
    if os.path.exists('threads_sub/' + identifier):
        os.unlink('threads_sub/' + identifier)

def subthread_clear():
    folder = 'threads_sub'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def subthread_identifier(_parent='x',_url=''):
    _index = 01
    _base = 'thread_' + _parent + '_' + _url
    m = hashlib.md5()
    m.update(_base)
    _base = str(m.hexdigest()) + '_'
    for i in range(1,500):
        _file = _base + str(_index) + '.session'
        if os.path.exists('threads_sub/' + _file):
            _index += 1
            continue
        else:
            f = open('threads_sub/' + _file,'w+')
            return _file

def subcrawl_links_export(_list,_identifier):
    with open('queue/' + _identifier, 'w') as f :
        f.write(json.dumps(_list))

def subcrawl_links_import(_identifier):
    with open('queue/' + _identifier, 'r') as f:
        _list = json.loads(f.read())
        return _list

def subcrawl_links_remove(_identifier):
    if os.path.exists('queue/' + _identifier):
        os.unlink('queue/' + _identifier)

def subcrawl_links_clear():
    folder = 'queue'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
