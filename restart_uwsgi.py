import os
import time

if __name__ == '__main__':
    ini = 'myFlask.ini'

    print('killing uwsgi')
    cmd_kill_uwsgi = "ps -ef | grep %s |  awk '{print $2}' | xargs kill -9" % ini
    os.system(cmd_kill_uwsgi)
    time.sleep(2)

    print('starting uwsgi')
    cmd_start_uwsgi = 'uwsgi %s' % ini
    os.system(cmd_start_uwsgi)
    time.sleep(2)

    print('uwsgi status:')
    cmd_uwsgi_status = 'ps -ef | grep %s' % ini
    os.system(cmd_uwsgi_status)
    time.sleep(1)

    print('--------finished----------')