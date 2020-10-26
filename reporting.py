import os
import datetime
import settings
import database

def init(_log=True):
    if _log:
        print('### Reporting module is online...')


# report types  : warning, error
# report levels : medium,important,critical
def report(report_type='warning', report_level='medium', position='', detail=''):
    _log_name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    _data = '{date:' + _log_name + '}\r\n' + '{type:' + report_type + '}\r\n' + '{priority:' + report_level + '}\r\n' + '{position:' + position + '}\r\n' + '{detail:\r\n' + detail + '\r\n}'

    _log_index = 0
    _found = False
    while not(_found):
        if os.path.exists('log/' + _log_name + '_' + str(_log_index) + '.txt'):
            _log_index+=1
        else:
            _log_name = _log_name + '_' + str(_log_index) + '.txt'
            _found = True


    with open('log/' + _log_name,'w+') as f:
        f.write(_data)
