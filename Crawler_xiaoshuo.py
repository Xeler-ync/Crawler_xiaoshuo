import re
import requests
import os
import datetime
import time
import sys

singleChapterOutPut=False
supportWebsitesNum=2
enabledWebsite=[True]*supportWebsitesNum
workingName=[]#用于分配工作时的缓存文件名

def writejianjie(contents,filePath):
    with open(sys.path[0]+'\\'+filePath,'a',encoding='utf-8') as ff:#创建jianjie
        ff.write(contents)
    return

def singleBookChapterCrawl(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng):#未完成
    if searchsite[realIndex]==0:#xsbiquge.com
        paxsbqgTraversalChapter(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng[realIndex])
    elif searchsite[realIndex]==1:#booktxt.net
        padingdianTraversalChapter(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng[realIndex])
    return

def singleBookzhuyeCrawl(tezheng,searchsite):
    if searchsite==0:#xsbiquge.com
        (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=paxsbqgzhuye(tezheng)
    elif searchsite==1:#booktxt.net
        (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=padingdianzhuye(tezheng[realIndex])
    return(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)

def selectBook(bookNames,tezheng,introduce,auther,searchsite,printToSource):
    while True:
        ipt=input().strip().lower()#获取指令
        num=re.findall('.([0-9]+)',ipt,re.S)#正则抓取数字
        if 'ls' in ipt or 'list' in ipt:#输出结果                            #参数识别
            for i in range(len(searchBookNames)):#遍历输出结果
                if i!=0 and searchBookNames[i]==searchBookNames[i-1]:#如果和存在重复则不输出
                    repetition+=1
                else:
                    print(str(i-repetition)+' '+searchBookNames[i])
        elif 'bk' in ipt or 'back' in ipt:#返回搜索
            return
        elif 'help' in ipt or '-h' in ipt or '-?' in ipt:#输出可用指令
            print('ls')
            print('List the title of the book\n')
            print('bk')
            print('Return to search\n')
            print('dt <num>')
            print('Show the details of the book\n')
            print('-scopt t/f')
            print('To enable/disable single chapter output.\n')
            print('pa <num>')
            print('Crawling book\n')
        elif 'dt' in ipt or 'detail' in ipt:#输出书本细节
            if int(num[0])>len(printToSource):
                print('Index out of range')
            realIndex=printToSource[int(num[0])]#将输出的序号对应到真实的列表index
            if '-d' in ipt:#进入书本主页爬取并输出细节
                if searchsite[realIndex]==0:#xsbiquge.com
                    (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=paxsbqgzhuye(tezheng[realIndex])
                elif searchsite[realIndex]==1:#booktxt.net
                    (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=padingdianzhuye(tezheng[realIndex])
                print('Title: 《'+zhuyebookname[0]+'》')
                print('Auther: '+zhuyebookauther[0])
                print(zhuyebookintroduction[0])
            else:#直接输出细节
                print('Title: 《'+bookNames[realIndex]+'》')
                print('Auther: '+auther[realIndex])
                print(introduce[realIndex])
        elif 'scopt' in ipt:#单章输出的选择
            ipt=ipt.replace('scopt','')
            if 't' in ipt or 'on' in ipt or '1' in ipt:#单章输出的选择
                global singleChapterOutPut
                singleChapterOutPut=True
            elif 'f' in ipt or 'off' in ipt or '0' in ipt:#单章输出的选择
                singleChapterOutPut=False
        elif 'pa' in ipt:#爬书
            realIndex=printToSource[int(num[0])]#将输出的序号对应到真实的列表index
            mutiSource=[]
            for i in range(len(bookNames)):#识别可能的多个来源
                if bookNames[i]==bookNames[realIndex]
                    mutiSource.append(realIndex)
            (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=singleBookzhuyeCrawl(tezheng[realIndex],searchsite[realIndex])


def paxsbqgSearchPage(keyword):
    searchHtmlResult=requests.get('https://www.xsbiquge.com/search.php?keyword='+keyword).content.decode('utf-8')#请求搜索数据
    searchHtmlResult=searchHtmlResult.replace('\t\t\t\t','')#除去不明所以的四个'\t'
    searchBookNames=re.findall('title="(.*?)" class="result-game-item-title-link" target="_blank">\r\n',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('<a cpos="title" href="https://www.xsbiquge.com/(.*?)/"',searchHtmlResult,re.S)#正则抓取网址
    searchIntroduce=re.findall('<p class="result-game-item-desc">(.*?)</p>\r\n',searchHtmlResult,re.S)#正则抓取简介
    searchAuther=re.findall('<span>\r\n                            (.*?)\r\n                        </span>',searchHtmlResult,re.S)#正则抓取作者
    print("Note: due to unknown reasons, we can't get all the results of xsbiquge.com's search interface")
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def paxsbqgzhuye(xiaoshuohao):#xsbiquge.com
    url="https://www.xsbiquge.com/"+xiaoshuohao+"/"
    html=requests.get(url).content.decode('utf-8')#请求数据
    emptychapter=re.findall('<dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>',html,re.S)#正则筛选   <dd><a href="/'+xiaoshuohao+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>
    for i in range(len(emptychapter)):#遍历去除
        html=html.replace(emptychapter[i],emptychapter[i].replace(' class="empty"',''))
    html_str=re.findall('<dd><a href="/'+xiaoshuohao+'/.*?.html">.*?</a></dd>',html,re.S)#正则抓取章节名与URL特征
    bookname=re.findall('/>\\r\\n<meta property="og:title" content="(.*?)"',html,re.S)#正则抓取书名
    bookauther=re.findall('/>\\r\\n<meta property="og:novel:author" content="(.*?)"',html,re.S)#正则抓取作者
    bookintroduction=re.findall('/>\r\n<meta property="og:description" content="(.*?)"',html,re.S)#正则抓取简介
    return(url,html_str,bookname,bookauther,bookintroduction)

def paxsbqgTraversalChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao):
    print(bookname[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入书名
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入作者
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入简介
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入获取的章节数
    with open(sys.path[0]+'\\results\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
        f.write('')#创建总文件
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入书名至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入作者至总文件
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入简介至总文件
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入获取的章节数至总文件
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    errorChapter=[]#用于记录出错章节名
    for i in range(len(html_str)):#遍历章节
        ii=i
        success=paxsbqgChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,ii)
        if success==True:
            print('\r'+'Completed: '+str(i)+'/'+str(len(html_str)-1), end='', flush=True)
        else:
            chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
            print('Error: '+chapterName[0])
            errorChapter.append(chapterName[0])
    endTime=datetime.datetime.now()
    deltaTime=(endTime-startTime).seconds
    print('\n'+str(deltaTime)+' seconds'+'    '+str(deltaTime/len(html_str))+' seconds per chapter\n')
    return errorChapter

def paxsbqgChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,i):
    writejianjie('\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入换行至总文件
    chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
    chapterFeature=re.findall('<dd><a href="/'+xiaoshuohao+'/(.*?).html',html_str[i],re.S)#获取章节URL特征
    chapterUrl='https://www.xsbiquge.com/'+xiaoshuohao+'/'+chapterFeature[0]+'.html'#拼接章节URL
    try:
        chapterName[0]=chapterName[0].replace('\\','[反斜杠]')#去除反斜杠
    except:#出错处理
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    chapterName[0]=chapterName[0].replace('/','[斜杠]')#去除斜杠
    chapterName[0]=chapterName[0].replace(':','[半角冒号]')#去除半角冒号
    chapterName[0]=chapterName[0].replace('*','[星号]')#去除星号
    chapterName[0]=chapterName[0].replace('?','[半角问号]')#去除半角问号
    chapterName[0]=chapterName[0].replace('"','[半角双引号]')#去除半角双引号
    chapterName[0]=chapterName[0].replace('<','[小于号]')#去除小于号
    chapterName[0]=chapterName[0].replace('>','[大于号]')#去除大于号
    chapterName[0]=chapterName[0].replace('|','[竖线]')#去除竖线
    try:
        chapter=requests.get(chapterUrl).content.decode('utf-8')#请求数据
    except:#出错处理
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    text=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>',chapter,re.S)#正则抓取正文  #<div id="content">
    try:
        text[0]=text[0].replace('<br />&nbsp;','') #去除无用html标签
    except:#出错处理
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
        writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        return False
    else :
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','\n')#处理换行
        if singleChapterOutPut==True:#是否输出单章
            with open(os.getcwd()+'\\'+bookname[0]+'\\'+chapterName[0]+'.txt','w',encoding='utf-8') as f:#创建f
                f.write(str(i)+' '+text[0])#写入正文与节号至分文件
        writejianjie(str(i)+' '+chapterName[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名与节号至总文件
        writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
        print('\r'+'Completed: '+str(i)+'/'+str(len(html_str)-1), end='', flush=True)
        return True

def padingdianSearchPage(keyword):#未完成
    keyword=keyword.encode('gbk')
    keyword=str(keyword).replace('\\x','%').replace("b'",'').replace("'",'')
    searchHtmlResult=requests.get('https://so.biqusoso.com/s1.php?siteid=booktxt.net&q='+str(keyword)).content.decode('utf-8')#请求搜索数据
    searchBookNames=re.findall('<span class="s2"><a href="http://www.booktxt.net/book/goto/id/.[0-9]+" target="_blank">(.*?)</a></span>',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('<span class="s2"><a href="http://www.booktxt.net/book/goto/id/(.[0-9]+)" target="_blank">.*?</a></span>',searchHtmlResult,re.S)#正则抓取网址
    for i in range (len(searchtezheng)):#为不存在的简介填充
        searchtezheng[i]=searchtezheng[i][0]+'_'+searchtezheng[i]
    searchIntroduce=[0 for i in range(len(searchBookNames))]
    for i in range(len(searchBookNames)):#处理特征以使之能被直接与URL组合
        searchIntroduce[i]=''
    searchAuther=re.findall('<span class="s4">(.[^<>]+)</span>',searchHtmlResult,re.S)#正则抓取作者
    #for i in range(len(searchtezheng)):#遍历输出结果
    #    print(str(i)+' '+searchBookNames[i])
    print("Note: booktxt.net will not display a introduction to each book on the search page")
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def padingdianzhuye(xiaoshuohao):#booktxt.net
    url='https://www.booktxt.net/'+xiaoshuohao+'/'
    html=requests.get(url).content.decode('gbk')#请求数据
    bookname=re.findall('<h1>(.*?)</h1>',html,re.S)#正则抓取书名
    bookauther=re.findall('<meta property="og:novel:author" content="(.*?)"/>',html,re.S)#正则抓取作者
    bookintroduction=re.findall('<meta property="og:description" content="(.*?)"/>',html,re.S)#正则抓取简介
    bookintroduction[0]=bookintroduction[0].replace(r'\r\n', "")
    garbage=re.findall('<!doctype html>.*<dt>《'+bookname[0]+'》正文',html,re.S)#顶点在正文前面有几个最新章节的链接，去除正文前面所有的内容
    html=html.replace(garbage[0],'')
    html_str=re.findall('<dd><a href ="[0-9]+.html">.*?</a></dd>\r\n\t\t',html,re.S)#正则抓取章节名与URL特征
    return(url,html_str,bookname,bookauther,bookintroduction)

def padingdianTraversalChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao):#未完成
    print(bookname[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')  #写入书籍相关信息至报告文件
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:  #创建总文件
        f.write('')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')  #写入书籍相关信息至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    errorChapter=[]#用于记录出错章节名
    for i in range(len(html_str)):#遍历章节
        ii=i
        success=padingdianChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,ii)
        if success==True:
            print('\r'+'Completed: '+str(i)+'/'+str(len(html_str)-1), end='', flush=True)
        else:
            chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
            print('Error: '+chapterName[0])
            errorChapter.append(chapterName[0])
    endTime=datetime.datetime.now()
    deltaTime=(endTime-startTime).seconds
    print('\n'+str(deltaTime)+' seconds'+'    '+str(deltaTime/len(html_str))+' seconds per chapter\n')
    return errorChapter

def padingdianChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao,i):
    writejianjie('\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入换行至总文件
    chapterName=re.findall('html">(.*?)</a></dd>',html_str[i],re.S)#正则抓取章节名
    chapterFeature=re.findall('<a href ="([0-9]+).html">',html_str[i],re.S)#获取章节URL特征
    chapterUrl='https://www.booktxt.net/'+xiaoshuohao+'/'+chapterFeature[0]+'.html'#拼接章节URL
    try:                                                                                                #不记得为什么要这么做了
        chapterName[0]=chapterName[0].replace('\\','[反斜杠]')#去除反斜杠
    except:#出错处理
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        writejianjie('Section '+str(i)+' unable to get chapter name'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入出错章节
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
        print('Error: Section'+i)
        return False
    else:
        chapterName[0]=chapterName[0].replace('/','[斜杠]')#去除斜杠
        chapterName[0]=chapterName[0].replace(':','[半角冒号]')#去除半角冒号
        chapterName[0]=chapterName[0].replace('*','[星号]')#去除星号
        chapterName[0]=chapterName[0].replace('?','[半角问号]')#去除半角问号
        chapterName[0]=chapterName[0].replace('"','[半角双引号]')#去除半角双引号
        chapterName[0]=chapterName[0].replace('<','[小于号]')#去除小于号
        chapterName[0]=chapterName[0].replace('>','[大于号]')#去除大于号
        chapterName[0]=chapterName[0].replace('|','[竖线]')#去除竖线
        while True:
            try:
                chapter=requests.get(chapterUrl).content.decode('gbk','ignore')#请求数据，dingdian偶尔会在正常的章节出现莫名其妙的非法字符，只能忽略，但是dingdian似乎只使用gbk所以看起来不会有什么问题
            except:
                chapter=''
            if chapter!='':
                break
    try: #如果出错意味着该章节没有内容
        text=re.findall('<div id="content">(.*?).[0-9!-<>]?<br /><br /><script>chaptererror()',chapter,re.S)#正则抓取正文，未能解决为什么会变为tuple而不是list
        text[0]=text[0][0]#将元组内容提出并重新为列表赋值
    except:#输出报告
        writejianjie('There is no content in section '+str(i)+'('+chapterName[0]+')'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
        writejianjie('There is no content in section '+str(i)+'('+chapterName[0]+')''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
        writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
        print('Error: '+chapterName[0])
        return False
    else:
        text[0]=text[0].replace('\u3000\u3000\u3000\u3000','\u3000\u3000')#替换四重空格
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','').replace('\r\r','\r')#处理换行
        if singleChapterOutPut==True:#是否输出单章
            with open(os.getcwd()+'\\'+bookname[0]+'\\'+chapterName[0]+'.txt','w',encoding='utf-8') as f:#创建f
                f.write(str(i)+' '+text[0])#写入正文与节号至分文件
        writejianjie(chapterName[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名至总文件
        writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
        return True

def getKeyWord():
    ipt=input('Please enter KeyWords: ')
    return ipt

def getbooks(keyWord):
    keyWord=keyWord

def initialiseSettings():#初始化全局变量
    global singleChapterOutPut
    singleChapterOutPut=False#单章输出
    enabledWebsite[0]=True#xsbiquge.com
    enabledWebsite[1]=True#booktxt.net

def changeSettings(ipt):#搜索时可配置的设置
    if '-h'in ipt or '-help'in ipt or '-?' in ipt:
        print('helps:')
        print('-scopt t/f\nTo enable/disable single chapter output.')
    elif 'scopt' in ipt:#单章输出的选择
        ipt=ipt.replace('scopt','')
        if 't' in ipt or 'on' in ipt or '1' in ipt:#单章输出的选择
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
            if websiteNum==0:#xsbiquge.comx
                searchingsite=0
                (searchBookNamesNew,searchtezhengNew,searchIntroduceNew,searchAutherNew)=paxsbqgSearchPage(ipt)
            elif websiteNum==1:#booktxt.net
                searchingsite=1
                (searchBookNamesNew,searchtezhengNew,searchIntroduceNew,searchAutherNew)=padingdianSearchPage(ipt)
            if len(searchBookNames)==0:#如果是第一次数据则直接赋值
                searchBookNames=searchBookNamesNew
                searchtezheng=searchtezhengNew
                searchIntroduce=searchIntroduceNew
                searchAuther=searchAutherNew
                searchsite=[searchingsite]*len(searchBookNames)
            else:#二次及以后后需要注意重复书名
                for indexOfNew in range(len(searchBookNamesNew)):#在搜索结果与原有结果之间遍历比对
                    if searchBookNames.count(searchBookNamesNew[indexOfNew])!=0:#出现重复书名则作为为其他来源
                        addingIndex=searchBookNames.index(searchBookNamesNew[indexOfNew])
                        searchBookNames.insert(addingIndex,searchBookNamesNew[indexOfNew])#加入至对应的书名index后面
                        searchtezheng.insert(addingIndex,searchtezhengNew[indexOfNew])
                        searchIntroduce.insert(addingIndex,searchIntroduceNew[indexOfNew])
                        searchAuther.insert(addingIndex,searchAutherNew[indexOfNew])
                        searchsite.insert(addingIndex,searchingsite)
                    else:
                        searchBookNames.append(searchBookNamesNew[indexOfNew])#反之则加入至末尾并进行下一个
                        searchtezheng.append(searchtezhengNew[indexOfNew])
                        searchIntroduce.append(searchIntroduceNew[indexOfNew])
                        searchAuther.append(searchAutherNew[indexOfNew])
                        searchsite.append(searchingsite)
    return searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchsite

def getzhuye(tezheng,sitenum):
    if sitenum==0:
        (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=paxsbqgzhuye(tezheng)
    elif sitenum==1:
        (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=padingdianzhuye(tezheng)
    return zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction

def chapterTraverse(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao)
    print(bookname[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookname[0])#以书名创建文件夹
        print('Create folder: '+bookname[0])
    except:
        print('Folder with the same name: "'+bookname[0]+'" already exists')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')  #写入书籍相关信息至报告文件
    writejianjie('Auther: '+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'.txt')
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:  #创建总文件
        f.write('')
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')  #写入书籍相关信息至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    errorChapter=[]#用于记录出错章节名
    #以下是v1.4的selectBook()中的爬书本
    if searchsite[int(num[0])]==0:#xsbiquge.com
        (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=paxsbqgzhuye(tezheng[int(num[0])])
        paxsbqgTraversalChapter(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng[int(num[0])])
    elif searchsite[int(num[0])]==1:#booktxt.net
        (zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction)=padingdianzhuye(tezheng[int(num[0])])
        padingdianTraversalChapter(zhuyeurl,zhuyehtml_str,zhuyebookname,zhuyebookauther,zhuyebookintroduction,tezheng[int(num[0])])
    return

initialiseSettings()
while True:
    (keyWord)=getKeyWord()
    if '-' in keyWord:
        changeSettings(keyWord)
    else:
        (searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchsite)=getBookSearchingResult(keyWord)
        repetition=0
        printToSource={}
        for i in range(len(searchBookNames)):#遍历输出结果
            if i!=0 and searchBookNames[i]==searchBookNames[i-1]:#如果和存在重复则不输出
                repetition+=1
            else:
                print(str(i-repetition)+' '+searchBookNames[i])
                printToSource[i-repetition]=i
        selectBook(searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchsite,printToSource)