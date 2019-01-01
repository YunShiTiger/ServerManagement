'''
在犹豫要不要加上软件管理的功能...
如果加的话，又再犹豫是用apt，yum这样的包管理器还是借用宝塔的安装shell脚本..
'''
from flask import request,render_template,redirect,url_for,session
import time
from index import app
import json
import os
import base64
import platform
import subprocess
import traceback
from .login import cklogin
class installPlugins:
    def __init__(self):
        self.systemVersionNub = None
        self.installProcess = {}
        self.pluginsList = [

        {'name':'nginx',
        'version':['1.10','1.12','1.14',"1.15",'1.8'],
        'subtext':'一款轻量级的Web服务器/反向代理服务器及电子邮件代理服务器,特点是占有内存少,并发能力强',
        'url':'/plugins/nginx'},

        {'name':'mysql',
        'version':['5.1','5.5','5.6','5.7','8.0','alisql','mariadb_5.5','mariadb_10.0','mariadb_10.1','mariadb_10.2','mariadb_10.3'],
        'subtext':'关系数据库管理系统,最流行的关系型数据库管理系统之一,所使用的SQL语言是用于访问数据库的最常用标准化语言',
        'url':'/plugins/mysql'},

        {'name':'pure-ftpd',
        'version':['1.0.47'],
        'subtext':'免费、安全、高质量和符合标准的FTP服务器,侧重于运行效率和易用性',
        'url':'/plugins/ftp'},

        {'name':'redis',
        'version':['5.0'],
        'subtext':'开源的使用ANSIC语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库',
        'url':'/plugins/redis'},

        {'name':'mongodb',
        'version':['3.6.3'],
        'subtext':'一个基于分布式文件存储的数据库，由C++语言编写。旨在为WEB应用提供可扩展的高性能数据存储解决方案',
        'url':'/plugins/mongodb'},

        {'name':'php',
        'version':['5.2','5.3','5.4','5.5','5.6','7.0','7.1','7.2','7.3'],
        'subtext':'最烂的语言',
        'url':'/plugins/php'}

        ]
        self.installFilePath = '/www/server/panel/install/install.sh'
        if 'LINUX' in platform.platform().upper():
            if os.path.exists('/etc/redhat-release'):
                self.systemVersionNub = '1' #centos
            elif os.path.exists('/etc/lsb-release'):
                self.systemVersionNub = '3' #ubuntu
        if self.systemVersionNub:
            if not os.path.isfile('/var/bt_setupPath.conf'):
                with open('/var/bt_setupPath.conf','w') as f:
                    f.write('/www')
            if not os.path.isdir('/www/server/panel/install/'):
                os.makedirs('/www/server/panel/install/')
                with open(self.installFilePath,'w') as f:
                    f.write('''#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
get_node_url(){
	nodes=(http://125.88.182.172:5880 http://103.224.251.67 http://128.1.164.196 http://download.bt.cn);
	i=1;
	for node in ${nodes[@]};
	do
		start=`date +%s.%N`
		result=`curl -sS --connect-timeout 3 -m 60 $node/check.txt`
		if [ "$result" = 'True' ];then
			end=`date +%s.%N`
			start_s=`echo $start | cut -d '.' -f 1`
			start_ns=`echo $start | cut -d '.' -f 2`
			end_s=`echo $end | cut -d '.' -f 1`
			end_ns=`echo $end | cut -d '.' -f 2`
			time_micro=$(( (10#$end_s-10#$start_s)*1000000 + (10#$end_ns/1000 - 10#$start_ns/1000) ))
			time_ms=$(($time_micro/1000))
			values[$i]=$time_ms;
			urls[$time_ms]=$node
			i=$(($i+1))
		fi
	done
	j=5000
	for n in ${values[@]};
	do
		if [ $j -gt $n ];then
			j=$n
		fi
	done
	if [ $j = 5000 ];then
		NODE_URL='http://download.bt.cn';
	else
		NODE_URL=${urls[$j]}
	fi
	
}

if [ ! $NODE_URL ];then
	get_node_url
fi

mtype=$1
actionType=$2
name=$3
version=$4
serverUrl=$NODE_URL/install

if [ ! -f 'lib.sh' ];then
	wget -O lib.sh $serverUrl/$mtype/lib.sh
fi

libNull=`cat lib.sh`
if [ "$libNull" == '' ];then
	wget -O lib.sh $serverUrl/$mtype/lib.sh
fi

wget -O $name.sh $serverUrl/$mtype/$name.sh
if [ "$actionType" == 'install' ];then
	bash lib.sh
fi
bash $name.sh $actionType $version
''')
    def install(self,name,version):
        if not self.systemVersionNub:
            return [False , '仅支持ubuntu及centos的软件安装']
        p={}
        for i in pluginsList:
            if i['name'] == name:
                p=i
                break
        else:
            return[False,'软件名不存在']
        if version not in p['version']:
            return[False,'版本错误']
        process = subprocess.Popen('cd /www/server/panel/install && /bin/bash %s %s %s %s %s' %(self.installFilePath,self.systemVersionNub,'install',name,version),
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        processNub = str(time.time())
        self.installProcess[processNub] = process
        return [True,processNub]
    def uninstall(self,name):
        subprocess.Popen('cd /www/server/panel/install && /bin/bash %s.sh uninstall' %name,
            shell=True)

Plugins = installPlugins()
@app.route('/plugins/GetPluginsList',methods=['POST'])
@cklogin()
def pluginsGetPluginsList():
    if not Plugins.systemVersionNub:
        return json.dumps({'resultCode':0,'result':[{'name':'仅支持Linux','url':'javascript:alert(\'软件管理仅支持Linux\')'}]})
    else:
        return json.dumps({'resultCode':0,'result':Plugins.pluginsList})
@app.route('/plugins/install',methods=['POST'])
@cklogin()
def PluginsInstall():
    name=request.values.get('name')
    version = request.values.get('version')
    installResult = Plugins.install(name,version)
    if not installResult[0]:
        return json.dumps({'resultCode':1,'result':installResult[1]})
    else:
        return json.dumps({'resultCode':0,'result':installResult[1]})

@app.route('/plugins/geiInstallState',methods=['POST'])
def geiInstallState():
    processNub = request.values.get('processNub')
    if processNub in Plugins.installProcess:
    	if Plugins.installProcess[processNub].poll() == None:
    	    return json.dumps({'resultCode':0,'result':installProcess[processNub].stdout.readline().decode()})
    	else:
    		del Plugins.installProcess[processNub]
    		return json.dumps({'resultCode':1})
    else:
    	return json.dumps({'resultCode':1,'result':'安装程序不存在或已经执行完毕'})




@app.route('/plugins/nginx',methods=['GET'])
@cklogin()
def pluginsNginx():
    if not Plugins.systemVersionNub:
        return json.dumps({'resultCode':1,'result':'本功能仅限linux'})
    if not os.path.isfile('/www/server/nginx/sbin/nginx'):
    	#未安装nginx或者并没有从本工具安装
    	return render_template('pluginsInstall.html',name='nginx')
    return render_template('NginxMange.html')
