from flask import request,render_template,redirect,url_for,session,Response
from index import app,url
import base64,platform,os,time,json,subprocess
from .login import cklogin
SYSTEMDEB = None
if 'LINUX' in platform.platform().upper():
    if os.path.exists('/etc/redhat-release'):
        SYSTEMDEB = 'yum' #centos
    elif os.path.exists('/etc/lsb-release'):
        SYSTEMDEB = 'apt' #ubuntu
if SYSTEMDEB:
    url.append( {"title": "软件管理",
        "children": [
            {"title": "nginx","href": "/plugins/nginx"}
            ]
        })
#---------------------------nginx------------------------------------------------#
NGINXSTATUS = None
@app.route('/plugins/nginx',methods=['GET','POST'])
@cklogin()
def pluginsNginx():
    global NGINXSTATUS
    if request.method == 'GET':
        if not NGINXSTATUS :
            status = subprocess.Popen(
                    'service nginx status',
                    shell=True,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
            status = status.stdout.read().decode()
            if ('unrecognized' in status) or ('could not be foun' in status):
                return render_template('plugins/pluginsInstall.html',name = 'nginx')
            else: 
                NGINXSTATUS = True
        return render_template('plugins/nginxMange.html')
    else:
        d = {'0':'start', '1':'stop','2':'reload','3':'restart','4':'status','5':'configtest'}
        nginxType = d.get(request.values.get('types'))
        if nginxType:
            shellResult = subprocess.Popen(
                    'service nginx %s'%nginxType,
                    shell=True,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
            return json.dumps({'resultCode':0,'result':shellResult.stdout.read().decode()})
        else:
            return json.dumps({'resultCode':1})
        
@app.route('/plugins/install/nginx',methods=['GET'])
@cklogin()
def pluginsinstallNginx():
    global NGINXSTATUS
    if NGINXSTATUS:
        return render_template('plugins/nginxMange.html')
    installScript = 'cd %s && /bin/bash %s' %(os.path.join(os.getcwd(),'lib/plugins/nginx/'),'nginx.sh')
    process = subprocess.Popen(
            installScript,
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    NGINXSTATUS = True
    def getNginxInfo(process):
        yield bytes("<h2>正在安装nginx...请稍等,安装完后会自动跳转...</h2>",'utf-8')
        while process.poll() == None:
            time.sleep(0.1)
            yield process.stdout.readline().replace(b'\n',b'<br>')
        yield bytes("<script>location.href = '/plugins/nginx'</script>",'utf-8')
    return Response(getNginxInfo(process))
#---------------------------nginx------------------------------------------------#
