# coding=utf-8

import os

c = get_config()


# logging file
c.Turing.extra_log_file = os.path.join('/tmp', 'turing_server.log')
c.Turing.listen_port = 9050

#生产环境中设为False;开发环境和测试环境中设为True
c.Turing.debug_switch = True


# DATABASE
mysql_db_name = "turing"
mysql_db_username = "pig"
mysql_db_passwd = "pig123"
mysql_db_server = "localhost"
c.Turing.db_url = "mysql+pymysql://%s:%s@%s/%s?charset=utf8" % (
    mysql_db_username, mysql_db_passwd, mysql_db_server, mysql_db_name)







