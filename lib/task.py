import datetime
import threading
import subprocess
import time
from index import sql
import os
import json
class taskset():
    def __init__(self):
        self.taskList=[]
        lastTask = sql.selectTask()
        if lastTask[0]:
            for i in lastTask[1]:
                self.CreatTask(json.loads(i[0]),writeToSql = False)
        else:
            print('从数据库恢复任务出错！')
        '''
        {'type':'day',
        'hour':'12',
        'mint':'30',
        'senc':'15',
        'creatTime'：'2018-12-3 19:48',
        'taskID':str(time.time()+random.random()),
        'nextRunTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+int(interval))),
        'value'："echo 666"
        },

        {'type':'week',
        'week':'0', #周日为0
        'hour':'12',
        'mint':'30',
        'senc':'15',
        'creatTime'：'2018-12-3 19:48',
        'taskID':str(time.time()+random.random()),
        'nextRunTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+int(interval))),
        'value'："echo 666"
        },

        {'type':'month',
        'day':'7',
        'hour':'12',
        'mint':'30',
        'senc':'15',
        'creatTime'：'2018-12-3 19:48',
        'taskID':str(time.time()+random.random()),
        'nextRunTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+int(interval))),
        'value'："echo 666"
        }


        '''
    def TaskFunc(self,data):
        if data not in self.taskList:
            return True
        self.taskList.remove(data)
        interval = self.GetNextTaskSenc(data)
        nowTime = data['nextRunTime']
        data['nextRunTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+int(interval)))
        timer = threading.Timer(interval, self.TaskFunc,(data,))
        timer.start()
        self.taskList.append(data)
        logname = 'lib/tasklog/'+data['creatTime'].replace(':','_')+'.log'
        with open(logname,'a') as f:
            f.write('-'*20+'\n'+nowTime+':\n')
        subprocess.Popen(data['value'],shell=True,stdout = open(logname,'a'),stderr = subprocess.STDOUT)

    def CreatTask(self,data,writeToSql=True):
        interval = self.GetNextTaskSenc(data)
        data['nextRunTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+int(interval)))
        self.taskList.append(data)
        if writeToSql:
            sql.insertTask(data)
        logname = 'lib/tasklog/'+data['creatTime'].replace(':','_')+'.log'
        if not os.path.isfile(logname):
            with open(logname,'w') as f:
                if data['type'] == 'day':
                    t = '每天的%s:%s:%s' %(data['hour'],data['mint'],data['senc'])
                elif data['type'] == 'month':
                    t = '每月%s号的%s:%s:%s' %(data['day'],data['hour'],data['mint'],data['senc'])
                elif data['type'] == 'week':
                    t = '每周%s的%s:%s:%s' %(data['week'],data['hour'],data['mint'],data['senc'])
                elif data['type'] == 'senc':
                    t = '每间隔%s秒' %data['senc']
                f.write('计划任务执行日志\n任务创建时间:%s\n计划类型:%s\nSHELL内容:%s\n'%(data['creatTime'],t,data['value']))
        timer = threading.Timer(interval, self.TaskFunc,(data,))
        timer.start()
    def GetTaskList(self):
        return self.taskList
    def DeleteTask(self,taskID):
        for i in self.taskList:
            if i['taskID'] == taskID:
                self.taskList.remove(i)
                sql.deleteTask(i['taskID'])
    def GetNextTaskSenc(self,data):
        if data['type'] == 'senc':
            return int(data['senc'])
            #设定周期不为秒的话,计算出下一次执行是几天之后
        elif data['type'] == 'day' :
            now_time = datetime.datetime.now()
            next_time = now_time + datetime.timedelta(days=1)
        elif data['type'] == 'week' :
            if str(data['week']) not in list(str(i) for i in range(0,8)):
                raise ValueError('日期设定错误,星期数值应在1-7内!')
            now_time = datetime.datetime.now()
            tip = 1  #从第二天计算,避免设定周几和今天相同,产生循环
            while True:
                next_time = now_time + datetime.timedelta(days=tip)
                if next_time.strftime('%w') == data['week']:
                    break
                else:
                    tip+=1
            next_time = now_time + datetime.timedelta(days=tip)
        elif data['type'] == 'month' :
            if str(data['day']) not in list(str(i) for i in range(1,32)):
                raise ValueError('日期设定错误,日期数值应在1-31内!')
            now_time = datetime.datetime.now()
            tip = 1 
            while True:
                next_time = now_time + datetime.timedelta(days=tip)
                if str(next_time.day) == str(data['day']):
                    break
                else:
                    tip+=1
            next_time = now_time + datetime.timedelta(days=tip)
        else:
            raise ValueError('无法解析下次执行的日期,请检查设定时间格式!')
        #下次执行任务的时间
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        try:
            #根据下次运行的时间,计算出秒数
            next_time = datetime.datetime.strptime('%s-%s-%s %s:%s:%s' %(next_year,next_month,next_day,data["hour"],data["mint"],data["senc"]), "%Y-%m-%d %H:%M:%S")
            timer_start_time = (next_time - now_time).total_seconds()
        except :
            raise ValueError('请检查时间格式!')
        return (int(timer_start_time)+1 if (timer_start_time%1 > 0) else int(timer_start_time)) #向上取整,只有这一个需求,懒得用math.ceil
