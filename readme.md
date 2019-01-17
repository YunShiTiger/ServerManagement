# ServerManagement
服务器管理工具，目前有文件管理器、进程监控、计划任务、webSSH、多主机管理、本地桌面、内网穿透等，后续会加入更多运维相关，本项目后端python+flask
## [更新日志](readme/更新日志.md)
## 功能介绍
### 1.文件管理
兼容windows和linxu的文件管理器,目前有文件的批量压缩、下载、重命名、文件内容在线编辑等. <br>
文件管理器中进行下载时,若下载的是文件,将会直接下载,若为目录,则会压缩为zip后下载 <br>
文件后缀为`.zip`,`.gz`,`.tar`的,可以在线解压 <br>
并提供一个批量文件操作的按钮,支持跨文件夹操作,后续可能会加入更多功能 <br>
### 2.进程监控
显示CPU、内存、磁盘状态,并实时显示网速 <br>
同时显示了进程以及网络进程,点击进程名可以查看进程详细信息 <br>
### 3.计划任务
可以设定以秒为单位的循环执行,也可以设定规则,如每周三的12:50:30,每月的23号15:30:00 <br>
### 4.shell
一个是个比较low的webSSH,最近可能没时间去完善这一块<br>
还有一个是多主机批量执行shell,支持root身份运行(目前很简陋,后续会添加更多功能)<br>
### 5.资源监控
本质上就是一个定时储存服务器资源使用情况的定时任务，前端请求到储存的数据后解析，最后用echarts生成折线图，为了尽量少的占用服务器资源，解析操作都是在网页前端进行的。<br>
### 6.便捷操作
现在只有一个快捷按钮的功能,就是可以自行设定一个常用的shll,方便快速调用,执行前可以做出修改,未来会加入其他我的脑洞...<br>
### 7.本地桌面
此功能仅限windows可用,所以并不默认开启,若有需要可在route/__init__.py中修改
### 8.内网穿透
选用功能,将项目下server.zip解压并在有外网IP的服务器上运行,在本地服务器管理工具运行时修改配置（外网服务器需要开启80端口，10000-20000端口，其中80端口为综合管理平台，可以查看所有的连接设备，可以查看其绑定的外网IP+端口，10000-20000端口为内网穿透的绑定端口）,即可实现内网穿透,在有外网IP的服务端上一键查看所有连接设备,后续会加入查看所有服务器实时状态等功能
## 项目截图
### 文件管理部分截图
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/文件管理.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/文件管理-选中.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/文件管理-编辑.png)
### 进程监控部分截图
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/进程监控-详细.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/进程监控-总览.png)
### 计划任务部分截图
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/计划任务.png)
### SSH部分截图
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/SSH.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/SSH链接.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/远程主机1.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/远程主机2.png)
### 资源监控部分截图(仍在完善中)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/资源监控.png)
### 快捷操作部分截图(仍在完善中)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/创建快捷按钮.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/查看已创建的快捷方式.png)
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/执行前查看.png)
### windows下本地桌面
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/本地桌面.png)
### 内网穿透+综合管理平台
![其余界面](https://github.com/cksgf/WebFileManager/blob/master/readme/内网穿透.png)
## 使用说明
### 运行本项目需要自行pip安装`flask`,`chardet`,`datetime`, `paramiko`,`pillow`,`psutil` <br>
### 或在目录下 python3 -m pip -r install requirements.txt<br>
以Ubuntu为例：
先安装python环境<br>
`apt install python3`<br>
`apt install python3-pip`<br>
然后安装依赖库<br>
`python3 -m pip install flask paramiko pillow datetime chardet pautil `<br>
最后进入项目运行就行了<br>
`python3 index.py`<br>
### route目录下是视图函数,目前有：
1.`file.py`,用来处理文件管理器的一些操作,<br>
2.`echarts`,用来完成前端图表的json传值,<br>
3.`process.py`,用来传递进程信息,<br>
4.`setTask.py`,设定、查询、删除计划任务,但是真正的计划任务操作是`/lib/task.py`来完成的，<br>
5.`webssh.py`,处理webSSH，多主机批量执行shell，先凑合用着，以后改进，<br>
6.`controlPanel.py`,处理资源监控的视图函数<br>
7.`linkButton.py`,常用shell的快捷方式<br>
8.`controlWin.py`,windows下本地桌面<br>
### lib目录下是一些功能的实现方法，<br>
1.`extract.py`,处理解压文件，目前只有.zip，.gz，.tar，如果有需要，可以在这添加方法，<br>
2.`task.py`,用于处理定时任务，这里我的实现方式是根据传入的定时类型和设定时间,计算出距离下一次符合时间的秒数，然后调用threading的Timer定时，定时函数执行时重新计算下一次时间，以此反复，<br>
3.`vieCode.py`,生成验证码,这份不是我自己写的,是从宝塔面板的代码里面抄来的= =,准备在写登录时用,目前暂时没用到<br>
4.`writeRes.py`,定时进行资源监控，并修改部分设置<br>
5.`common_func.py`,`slaver.py`为实现内网穿透功能的文件<br>
### config目录用于配制程序
`config.py`,里面定义了以下内容：<br>
1.文件管理器应该从那个目录开始显示,一般为'/'就好。<br>
2.资源监控默认开关/最大储存时间/前端默认显示时间/后台记录间隔。 <br>
### sqlitedb是数据库目录
`sqlitedb.py`,处理数据库操作<br>
## 本项目后端给前端传值全部使用json,前端用jq处理、发送请求并生成最终页面<br>
## 其中的文件管理器部分前端给后端传值,大部分采用base64编码 <br>
## 使用前切记修改config/config<br>

