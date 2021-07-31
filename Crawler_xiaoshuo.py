import re
import requests
import os
import datetime
import time
import sys

singleChapterOutPut=False
supportWebsitesNum=1#增添网站时记得改这里
enabledWebsite=[True]*supportWebsitesNum

def writejianjie(contents,filePath):
    with open(sys.path[0]+'\\'+filePath,'a',encoding='utf-8') as ff:#创建jianjie
        ff.write(contents)
    return

def selectBook(bookNames,tezheng,introduce,auther,searchsite):
    while True:
        ipt=input().strip().lower()#获取指令
        num=re.findall('.([0-9]+)',ipt,re.S)#正则抓取数字
        if 'ls' in ipt or 'list' in ipt:#输出结果                            #参数识别
            for i in range(len(bookNames)):
               print(str(i)+' '+bookNames[i])
        elif 'bk' in ipt or 'back' in ipt:#返回搜索
            return
        elif 'help' in ipt or '-h' in ipt or '-?' in ipt:#输出可用指令
            print('ls\n')
            print('List the title of the book\n')
            print('bk\n')
            print('Return to search\n')
            print('dt <num>\n')
            print('Show the details of the book\n')
            print('helps:')
            print('-scopt t/f\nTo enable/disable single chapter output.')
            print('pa <num>\n')
            print('Crawling book\n')
        elif 'dt' in ipt or 'detail' in ipt:#输出书本细节
            if int(num[0])>len(tezheng):
                print('Index out of range')
            if '-d' in ipt:#进入书本主页爬取并输出细节
                if searchsite[int(num[0])]==0:#vbiquge.com
                    (zhuyeurl,zhuyeBookChapterFeature,zhuyeBookChapterName,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=pavbiqugezhuye(tezheng[int(num[0])])
                print('Title: 《'+zhuyebookname[0]+'》')
                print('Auther: '+zhuyebookauther[0])
                print(zhuyebookintroduction[0])
            else:#直接输出细节
                print('Title: 《'+bookNames[int(num[0])]+'》')
                print('Auther: '+auther[int(num[0])])
                print(introduce[int(num[0])])
        elif 'scopt' in ipt:#单章输出的选择
            ipt=ipt.replace('scopt','')
            if 't' in ipt or 'on' in ipt or '1' in ipt:#单章输出的选择
                global singleChapterOutPut
                singleChapterOutPut=True
            elif 'f' in ipt or 'off' in ipt or '0' in ipt:#单章输出的选择
                singleChapterOutPut=False
        elif 'pa' in ipt:#爬书
            if searchsite[int(num[0])]==0:#vbiquge.com
                (zhuyeurl,zhuyeBookChapterFeature,zhuyeBookChapterName,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=pavbiqugezhuye(tezheng[int(num[0])])
                pavbiqugeTraversalChapter(zhuyeurl,zhuyeBookChapterFeature,zhuyeBookChapterName,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng[int(num[0])])
            return

def pavbiqugeSearchPage(keyword):
    searchHtmlResult=requests.get('https://www.vbiquge.com/search.php?keyword='+keyword).content.decode('utf-8')#请求搜索数据
    searchHtmlResult=searchHtmlResult.replace('\t\t\t\t','')#除去不明所以的四个'\t'
    searchBookNames=re.findall('title="(.*?)" class="result-game-item-title-link" target="_blank">\r\n',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('<a cpos="title" href="https://www.vbiquge.com/(.*?)/"',searchHtmlResult,re.S)#正则抓取网址
    searchIntroduce=re.findall('<p class="result-game-item-desc">(.*?)</p>\r\n',searchHtmlResult,re.S)#正则抓取简介
    searchAuther=re.findall('<span>\r\n                            (.*?)\r\n                        </span>',searchHtmlResult,re.S)#正则抓取作者
    print("Note: due to unknown reasons, we can't get all the results of vbiquge.com's search interface")
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def pavbiqugezhuye(xiaoshuohao):#vbiquge.com
    url="https://www.vbiquge.com/"+xiaoshuohao+"/"
    html=requests.get(url).content.decode('utf-8')#请求数据
    #这是用于 xsbiquge.com 的代码， vbiquge.com 看起来是从她继承而来，不确定这几行代码是否有用
    #emptychapter=re.findall('<dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>',html,re.S)#正则筛选   <dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>
    #for i in range(len(emptychapter)):#遍历去除
    #    html=html.replace(emptychapter[i],emptychapter[i].replace(' class="empty"',''))
    bookChapterFeature=re.findall('<dd><a href="/'+xiaoshuohao+'/(.*?).html">.*?</a></dd>',html,re.S)#正则抓取章节名与URL特征
    bookChapterName=re.findall('<dd><a href="/'+xiaoshuohao+'/.*?.html">(.*?)</a></dd>',html,re.S)#正则抓取章节名与URL特征
    bookname=re.findall('/>\\r\\n<meta property="og:title" content="(.*?)"',html,re.S)#正则抓取书名
    bookauther=re.findall('/>\\r\\n<meta property="og:novel:author" content="(.*?)"',html,re.S)#正则抓取作者
    bookintroduction=re.findall('/>\r\n<meta property="og:description" content="(.*?)"',html,re.S)#正则抓取简介
    return(url,bookChapterFeature,bookChapterName,bookname,bookauther,bookintroduction)


def pavbiqugeTraversalChapter(url,bookChapterFeature,bookChapterName,bookname,bookauther,bookintroduction,xiaoshuohao):
    print(bookname[0])
    print(str(len(bookChapterFeature))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入书名
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入作者
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入简介
    writejianjie('Possible chapters: '+str(len(bookChapterFeature))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入获取的章节数
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
        f.write('')#创建总文件
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入书名至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入作者至总文件
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入简介至总文件
    writejianjie('Possible chapters: '+str(len(bookChapterFeature))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入获取的章节数至总文件
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    for i in range(len(bookChapterFeature)):#遍历章节
        ii=i
        success=pavbiqugeChapter(url,bookChapterFeature,bookChapterName,bookname,bookauther,bookintroduction,xiaoshuohao,ii)
        if success==True:
            print('\r'+'Completed: '+str(i)+'/'+str(len(bookChapterFeature)-1), end='', flush=True)
        else:
            print('Error: '+bookChapterName[i])
    endTime=datetime.datetime.now()
    deltaTime=(endTime-startTime).seconds
    print('\n'+str(deltaTime)+' seconds'+'    '+str(deltaTime/len(bookChapterFeature))+' seconds per chapter\n')

def pavbiqugeChapter(url,chapterFeature,chapterName,bookname,bookauther,bookintroduction,xiaoshuohao,i):
    writejianjie('\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入换行至总文件
    chapterUrl='https://www.vbiquge.com/'+xiaoshuohao+'/'+chapterFeature[i]+'.html'#拼接章节URL
    try:
        chapterName[i]=chapterName[i].replace('\\','[反斜杠]')#去除反斜杠
    except:#出错处理
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    chapterName[i]=chapterName[i].replace('/','[斜杠]')#去除斜杠
    chapterName[i]=chapterName[i].replace(':','[半角冒号]')#去除半角冒号
    chapterName[i]=chapterName[i].replace('*','[星号]')#去除星号
    chapterName[i]=chapterName[i].replace('?','[半角问号]')#去除半角问号
    chapterName[i]=chapterName[i].replace('"','[半角双引号]')#去除半角双引号
    chapterName[i]=chapterName[i].replace('<','[小于号]')#去除小于号
    chapterName[i]=chapterName[i].replace('>','[大于号]')#去除大于号
    chapterName[i]=chapterName[i].replace('|','[竖线]')#去除竖线
    try:
        chapter=requests.get(chapterUrl).content.decode('utf-8')#请求数据
    except:#出错处理
        writejianjie('Section '+str(i)+'('+chapterName[i]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
        writejianjie('Section '+str(i)+'('+chapterName[i]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    text=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>',chapter,re.S)#正则抓取正文  #<div id="content">
    try:
        text[0]=text[0].replace('<br />&nbsp;','') #去除无用html标签
    except:#出错处理
        writejianjie('Section '+str(i)+'('+chapterName[i]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
        writejianjie('Section '+str(i)+'('+chapterName[i]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    else :
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','\n')#处理换行
        if singleChapterOutPut==True:#是否输出单章
            with open(os.getcwd()+'\\'+bookname[0]+'\\'+chapterName[i]+'.txt','w',encoding='utf-8') as f:#创建f
                f.write(str(i)+' '+text[0])#写入正文与节号至分文件
        writejianjie(str(i)+' '+chapterName[i]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名与节号至总文件
        writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
        print('\r'+'Completed: '+str(i)+'/'+str(len(chapterFeature)-1), end='', flush=True)
        return True

def getKeyWord():
    ipt=input('Please enter KeyWords: ')
    return ipt

def initialiseSettings():#初始化全局变量
    global singleChapterOutPut
    singleChapterOutPut=False#单章输出
    enabledWebsite[0]=True#vbiquge.com

def changeSettings(ipt):#搜索时可配置的设置
    if '-h'in ipt or '-help'in ipt or '-?' in ipt:
        print('helps:')
        print('-scopt t/f\nTo enable/disable single chapter output.')
    elif '-scopt' in ipt:#单章输出的选择
        ipt=ipt.replace('scopt','')
        if ' t' in ipt or 'on' in ipt or '1' in ipt:#单章输出的选择
            global singleChapterOutPut
            singleChapterOutPut=True
        elif 'f' in ipt or 'off' in ipt or '0' in ipt:#单章输出的选择
            singleChapterOutPut=False

def getBookSearchingResult(ipt):#获取各个网址的搜索结果
    searchBookNames=[]#初始化变量
    searchtezheng=[]
    searchIntroduce=[]
    searchAuther=[]
    searchsite=[]
    searchingsite=0
    for websiteNum in range(supportWebsitesNum):#遍历可用的网站
        if enabledWebsite[websiteNum]:
            if websiteNum==0:#vbiquge.comx
                searchingsite=0
                (searchBookNamesNew,searchtezhengNew,searchIntroduceNew,searchAutherNew)=pavbiqugeSearchPage(ipt)
            if len(searchBookNames)==0:#如果是第一次数据则直接赋值
                searchBookNames=searchBookNamesNew
                searchtezheng=searchtezhengNew
                searchIntroduce=searchIntroduceNew
                searchAuther=searchAutherNew
                searchsite=[searchingsite]*len(searchBookNames)
            else:#二次及以后后需要注意重复书名
                for indexOfNew in range(len(searchBookNamesNew)):#在搜索结果与原有结果之间遍历比对
                    if searchBookNames.count(searchBookNamesNew[indexOfNew])!=0:#出现重复书名则跳过
                        continue
                    else:
                        searchBookNames.append(searchBookNamesNew[indexOfNew])#反之则加入至末尾并进行下一个
                        searchtezheng.append(searchtezhengNew[indexOfNew])
                        searchIntroduce.append(searchIntroduceNew[indexOfNew])
                        searchAuther.append(searchAutherNew[indexOfNew])
                        searchsite.append(searchingsite)
    return searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchsite

initialiseSettings()
while True:
    (keyWord)=getKeyWord()
    if '-' in keyWord:
        changeSettings(keyWord)
    else:
        (searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchsite)=getBookSearchingResult(keyWord)
        for i in range(len(searchBookNames)):#遍历输出结果
            print(str(i)+' '+searchBookNames[i])
        selectBook(searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchsite)