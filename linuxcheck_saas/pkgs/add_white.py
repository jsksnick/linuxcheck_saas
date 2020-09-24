# -*- coding: utf-8 -*-
import commands

try:
    import pymysql
except:
    pass
APP_ID = "ad-sec_saas"
ENV_ARR = []


class OpenPaas(object):
    def __init__(self):
        self.db = self._connect()

    def add_white_name(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("select wlist from esb_function_controller where func_code='user_auth::skip_user_auth'")
            data = cursor.fetchone()
            wlist = data[0]
            app_ids = wlist.split(',')
            if APP_ID not in app_ids:
                app_ids.append(APP_ID)
            wlist = ','.join(app_ids)
            cursor.execute('UPDATE esb_function_controller SET wlist="{}"'.format(wlist))
        except Exception as e:
            print '添加白名单失败{0}'.format(e.message)

    def add_env(self):
        try:
            cursor = self.db.cursor()
            for env in ENV_ARR:
                cursor.execute(
                    'select * from paas_app_envvars where `app_code`="{0}" and `name`="{1}"'.format(
                        APP_ID, env['env_key']
                    )
                )
                res = cursor.fetchall()
                if len(res):
                    continue
                insert_sql = 'INSERT INTO paas_app_envvars (`app_code`,`name`,`value`,`mode`,`intro`) VALUES ("{0}","{1}","{2}","{3}","{4}")'.format(
                    APP_ID,
                    env['env_key'],
                    env['examples'],
                    'all',
                    env['desc']
                )
                cursor.execute("set names 'utf8'")
                cursor.execute(insert_sql)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            print '添加环境变量失败{}'.format(e.message)

    def _connect(self):
        info = self._get_mysql_info()
        db = pymysql.connect(info['host'], info['user'], info['pwd'], 'open_paas')
        return db

    def __del__(self):
        self.db.close()

    def _get_mysql_info(self):
        return {
            'host': "192.168.165.51",
            'pwd': 'bk@321',
            'user': 'root'
        }
        command = """
mysql_ip=$(cat /data/install/install.config|grep mysql|head -1|awk '{print $1}')
mysql_user=$(cat /data/install/globals.env |grep MYSQL_USER|sed -r 's/.*(MYSQL_USER=[^ ]+).*/\1/'|cut -d'=' -f2|grep -o '[^"]\+\( \+[^"]\+\)*')
mysql_pwd=$(cat /data/install/globals.env |grep MYSQL_PASS|sed -r 's/.*(MYSQL_PASS=[^ ]+).*/\1/'|cut -d'=' -f2|grep -o '[^"]\+\( \+[^"]\+\)*')
echo {'"'host'"': '"'$mysql_ip'"',\
      '"'user'"': '"'$mysql_user'"',\
      '"'pwd'"': '"'$mysql_pwd'"'\
}
"""
        return eval(self._execute(command))

    def check_paas_type(self):
        command = """
if [ -d "/data/bkee" ];then
    echo bkee
elif [ -d "/data/bkce" ];then
    echo bkce
else
    echo no
fi
"""
        return self._execute(command)

    def _execute(self, command):
        code, output = commands.getstatusoutput(command)
        if str(code) != '0':
            assert 'update env or white name error:{0}'.format(output)
        return output.strip().strip("\n")


if __name__ == '__main__':
    o = OpenPaas()
    o.add_env()
