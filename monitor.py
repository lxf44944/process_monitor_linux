# -*- coding: utf-8 -*-
import os
import urllib
import time
import sys
import codecs
import string

reload(sys)
sys.setdefaultencoding( "utf-8" )

partLable = ("<",">")
sectionLable = ("[","]")
#endlineLable = "\r\n" # windows下的行标志
endlineLable = "\n"   # linux下的行标志
equalLable = "=" # 赋值标志
noteLable = '#' # 注释标志

# 得到总配置的map
def getPlatformMap(strtmp,lable1 = partLable,lable2 = sectionLable):
    tmp = strtmp.split(lable1[0])
    tmp = [elem for elem in tmp if len(elem) > 1]
    tmp = [elem for elem in tmp if elem.rfind(lable1[1]) > 0]
    platdict = {}
    for elem in tmp:
        key = elem[0:elem.find(lable1[1]):]
        value = elem[elem.find(lable2[0])::]
        platdict[key] = value
    return platdict

# 得到各部分的map
def getSectionMap(strtmp,lable1 = sectionLable):
    tmp = strtmp.split(lable1[0])
    tmp = [elem for elem in tmp if len(elem) > 1]
    tmp = [elem for elem in tmp if elem.rfind(lable1[1]) > 0]
    sectionDict = {}
    for elem in tmp:
        key = elem[0:elem.find(lable1[1]):]
        value = elem[elem.find(endlineLable)+len(endlineLable)::]
        sectionDict[key] = value
    return sectionDict

# 获取具体配置值
def getValueMap(strtmp):
    tmp = strtmp.split(endlineLable)
    tmp = [elem for elem in tmp if len(elem) > 1]
    valueDict = {}
    for elem in tmp:
        if elem.find(noteLable) > 0: # 如果有注释则去掉注释
            elem = elem[0:elem.find(noteLable):]
        elem = ''.join(elem.split()) # 去掉空白字符  
        key = elem[0:elem.find(equalLable):]
        value = elem[elem.find(equalLable)+len(equalLable)::]
        valueDict[key] = value
    return valueDict

def getinit():
    f = open('monitor.ini')
    strFileContent = f.read()
    f.close()
    vardict = {}

    var1 = getPlatformMap(strFileContent)

    for k,v in var1.items():
        var2 = getSectionMap(v)
        dict3 = {}
        for k2,v2 in var2.items():
            var3 = getValueMap(v2)
            dict3[k2] = var3
        vardict[k] = dict3

    return vardict

def check(paramdict):
    #get the system calender
    t = time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year = t[0]
    month = t[1]
    day = t[2]
    #get the name of file
    dir='/data3/gpsdata/'+str(year)+'/'+str(month)+'/'+str(year)+str(month)+str(day)+'.txt'
    print dir
    if not os.path.exists(dir):                                     ##
        os.system('/root/tcp2udp/tcp2udp')#start process
        time.sleep(60)                                              ##
        print 'first restart finished'
        if not os.path.exists(dir):                                 ##
            os.system('/root/tcp2udp/tcp2udp')#start process
            time.sleep(60)                                          ##
            print 'second restart finished'
        if not os.path.exists(dir):    #fail                        ##
            print 'restart failed'
            for param in paramdict.values():
                #print param['param']
                params = urllib.urlencode(param['param'])      
                urllib.urlopen("http://127.0.0.1:8080/sms", params)
        else:    #success
            print 'restart success'
            for param in paramdict.values():
                #print param['param']
                params = urllib.urlencode(param['paramsuc'])      
                urllib.urlopen("http://127.0.0.1:8080/sms", params)

if __name__ == '__main__':
    while(True):
        paramdict = getinit()
        #print paramdict.values()
        check(paramdict)
        time.sleep(60*60)  #every 1 hour
