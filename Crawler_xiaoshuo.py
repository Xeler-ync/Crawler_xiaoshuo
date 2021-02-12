import re
import requests
import os
import datetime
import time
import sys

singleChapterOutPut=False
supportWebsitesNum=2
enabledWebsite=[True]*supportWebsitesNum

def writejianjie(contents,filePath):
    with open(sys.path[0]+'\\'+filePath,'a',encoding='utf-8') as ff:#创建jianjie
        ff.write(contents)
    return

def selectBook(bookNames,tezheng,introduce,auther,searchSite,printToSource):
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
                if searchSite[realIndex]==0:#xsbiquge.com
                    (zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)=paxsbqgzhuye(tezheng[realIndex])
                elif searchSite[realIndex]==1:#booktxt.net
                    (zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)=padingdianzhuye(tezheng[realIndex])
                del zhuyeurl#删掉变量省着报错
                del zhuyehtml_str
                print('Title: 《'+zhuyeBookName[0]+'》')
                print('Auther: '+zhuyeBookAuther[0])
                print(zhuyeBookIntroduction[0])
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
            tezhengList=[]
            searchsiteList=[]
            for i in range(len(bookNames)):#识别可能的多个来源
                if bookNames[i]==bookNames[realIndex]:
                    tezhengList.append(bookNames[realIndex])
                    searchsiteList.append(searchSite[realIndex])
            return tezhengList,searchsiteList

def paxsbqgSearchPage(keyword):
    searchHtmlResult=requests.get('https://www.xsbiquge.com/search.php?keyword='+keyword).content.decode('utf-8')#请求搜索数据
    searchHtmlResult=searchHtmlResult.replace('\t\t\t\t','')#除去不明所以的四个'\t'
    searchBookNames=re.findall('title="(.*?)" class="result-game-item-title-link" target="_blank">\r\n',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('<a cpos="title" href="https://www.xsbiquge.com/(.*?)/"',searchHtmlResult,re.S)#正则抓取网址
    searchIntroduce=re.findall('<p class="result-game-item-desc">(.*?)</p>\r\n',searchHtmlResult,re.S)#正则抓取简介
    searchAuther=re.findall('<span>\r\n                            (.*?)\r\n                        </span>',searchHtmlResult,re.S)#正则抓取作者
    print("Note: due to unknown reasons, we can't get all the results of xsbiquge.com's search interface")
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def paxsbqgzhuye(tezheng):#xsbiquge.com
    url="https://www.xsbiquge.com/"+tezheng+"/"
    html=requests.get(url).content.decode('utf-8')#请求数据
    emptychapter=re.findall('<dd><a href="/'+tezheng+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>',html,re.S)#正则筛选   <dd><a href="/'+tezheng+'/.[0-9]+?.html" class="empty">本站重要通告</a></dd>
    for i in range(len(emptychapter)):#遍历去除
        html=html.replace(emptychapter[i],emptychapter[i].replace(' class="empty"',''))
    html_str=re.findall('<dd><a href="/'+tezheng+'/.*?.html">.*?</a></dd>',html,re.S)#正则抓取章节名与URL特征
    bookName=re.findall('/>\\r\\n<meta property="og:title" content="(.*?)"',html,re.S)#正则抓取书名
    bookAuther=re.findall('/>\\r\\n<meta property="og:novel:author" content="(.*?)"',html,re.S)#正则抓取作者
    bookIntroduction=re.findall('/>\r\n<meta property="og:description" content="(.*?)"',html,re.S)#正则抓取简介
    return(url,html_str,bookName,bookAuther,bookIntroduction)

def paxsbqgTraversalChapter(url,html_str,bookName,bookAuther,bookIntroduction,tezheng):
    print(bookName[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookName[0])#以书名创建文件夹
        print('Create folder: '+bookName[0])
    except:
        print('Folder with the same name: "'+bookName[0]+'" already exists')
    writejianjie('《'+bookName[0]+'》'+'\n',bookName[0]+'\\'+bookName[0]+'.txt')#写入书名
    writejianjie('Auther: '+bookAuther[0]+'\n',bookName[0]+'\\'+bookName[0]+'.txt')#写入作者
    writejianjie('    '+bookIntroduction[0]+'\n',bookName[0]+'\\'+bookName[0]+'.txt')#写入简介
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookName[0]+'\\'+bookName[0]+'.txt')#写入获取的章节数
    with open(sys.path[0]+'\\results\\'+bookName[0]+'\\'+bookName[0]+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
        f.write('')#创建总文件
    writejianjie('《'+bookName[0]+'》'+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')#写入书名至总文件
    writejianjie('Auther :'+bookAuther[0]+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')#写入作者至总文件
    writejianjie('    '+bookIntroduction[0]+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')#写入简介至总文件
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')#写入获取的章节数至总文件
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    errorChapter=[]#用于记录出错章节名
    for i in range(len(html_str)):#遍历章节
        success=paxsbqgChapter(html_str,tezheng)
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

def paxsbqgChapter(html_str,tezheng):
    chapterFeature=re.findall('<dd><a href="/'+tezheng+'/(.*?).html',html_str,re.S)#获取章节URL特征
    chapterUrl='https://www.xsbiquge.com/'+tezheng+'/'+chapterFeature[0]+'.html'#拼接章节URL
    try:
        chapter=requests.get(chapterUrl).content.decode('utf-8')#请求数据
    except:#出错处理
        return False
    text=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>',chapter,re.S)#正则抓取正文  #<div id="content">
    try:
        text[0]=text[0].replace('<br />&nbsp;','') #去除无用html标签
    except:#出错处理
        return False
    else :
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','\n')#处理换行
        return text[0]

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

def padingdianzhuye(tezheng):#booktxt.net
    url='https://www.booktxt.net/'+tezheng+'/'
    html=requests.get(url).content.decode('gbk')#请求数据
    bookName=re.findall('<h1>(.*?)</h1>',html,re.S)#正则抓取书名
    bookAuther=re.findall('<meta property="og:novel:author" content="(.*?)"/>',html,re.S)#正则抓取作者
    bookIntroduction=re.findall('<meta property="og:description" content="(.*?)"/>',html,re.S)#正则抓取简介
    bookIntroduction[0]=bookIntroduction[0].replace(r'\r\n', "")
    garbage=re.findall('<!doctype html>.*<dt>《'+bookName[0]+'》正文',html,re.S)#顶点在正文前面有几个最新章节的链接，去除正文前面所有的内容
    html=html.replace(garbage[0],'')
    html_str=re.findall('<dd><a href ="[0-9]+.html">.*?</a></dd>\r\n\t\t',html,re.S)#正则抓取章节名与URL特征
    return(url,html_str,bookName,bookAuther,bookIntroduction)

def padingdianTraversalChapter(url,html_str,bookName,bookAuther,bookIntroduction,tezheng):#未完成
    print(bookName[0])
    print(str(len(html_str))+' in total')
    try:
        os.mkdir(bookName[0])#以书名创建文件夹
        print('Create folder: '+bookName[0])
    except:
        print('Folder with the same name: "'+bookName[0]+'" already exists')
    writejianjie('《'+bookName[0]+'》'+'\n',bookName[0]+'\\'+bookName[0]+'.txt')  #写入书籍相关信息至报告文件
    writejianjie('Auther: '+bookAuther[0]+'\n',bookName[0]+'\\'+bookName[0]+'.txt')
    writejianjie('    '+bookIntroduction[0]+'\n',bookName[0]+'\\'+bookName[0]+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookName[0]+'\\'+bookName[0]+'.txt')
    with open(sys.path[0]+'\\'+bookName[0]+'\\'+bookName[0]+'_总'+'.txt','w',encoding='utf-8') as f:  #创建总文件
        f.write('')
    writejianjie('《'+bookName[0]+'》'+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')  #写入书籍相关信息至总文件
    writejianjie('Auther :'+bookAuther[0]+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')
    writejianjie('    '+bookIntroduction[0]+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    errorChapter=[]#用于记录出错章节名
    for i in range(len(html_str)):#遍历章节
        success=padingdianChapter(html_str,tezheng)
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

def padingdianChapter(html_str,tezheng):
    chapterFeature=re.findall('<a href ="([0-9]+).html">',html_str,re.S)#获取章节URL特征
    chapterUrl='https://www.booktxt.net/'+tezheng+'/'+chapterFeature[0]+'.html'#拼接章节URL
    chapter='false'
    while chapter:#dingdian有时会莫名其妙无法获取，但是每一个章节必定有html内容，故使用while
        try:
            chapter=requests.get(chapterUrl).content.decode('gbk','ignore')#请求数据，dingdian偶尔会在正常的章节出现莫名其妙的非法字符，只能忽略，但是dingdian似乎只使用gbk所以看起来不会有什么问题
        except:
            chapter=''
    try: #如果出错意味着该章节没有内容
        text=re.findall('<div id="content">(.*?).[0-9!-<>]?<br /><br /><script>chaptererror()',chapter,re.S)#正则抓取正文，未能解决为什么会变为tuple而不是list
        text[0]=text[0][0]#将元组内容提出并重新为列表赋值
    except:#输出报告
        return False
    else:
        text[0]=text[0].replace('\u3000\u3000\u3000\u3000','\u3000\u3000')#替换四重空格
        text[0]=text[0].replace('&nbsp;','')#去除无用html标签
        text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
        text[0]=text[0].replace('<br />','').replace('\r\r','\r')#处理换行
        return text[0]

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
    searchSite=[]
    for websiteNum in range(supportWebsitesNum):#遍历可用的网站
        if enabledWebsite[websiteNum]:
            if websiteNum==0:#xsbiquge.comx
                (searchBookNamesNew,searchtezhengNew,searchIntroduceNew,searchAutherNew)=paxsbqgSearchPage(ipt)
            elif websiteNum==1:#booktxt.net
                (searchBookNamesNew,searchtezhengNew,searchIntroduceNew,searchAutherNew)=padingdianSearchPage(ipt)
            if len(searchBookNames)==0:#如果是第一次数据则直接赋值
                searchBookNames=searchBookNamesNew
                searchtezheng=searchtezhengNew
                searchIntroduce=searchIntroduceNew
                searchAuther=searchAutherNew
                searchSite=[searchSite]*len(searchBookNames)
            else:#二次及以后后需要注意重复书名
                for indexOfNew in range(len(searchBookNamesNew)):#在搜索结果与原有结果之间遍历比对
                    if searchBookNames.count(searchBookNamesNew[indexOfNew])!=0:#出现重复书名则作为为其他来源
                        addingIndex=searchBookNames.index(searchBookNamesNew[indexOfNew])
                        searchBookNames.insert(addingIndex,searchBookNamesNew[indexOfNew])#加入至对应的书名index后面
                        searchtezheng.insert(addingIndex,searchtezhengNew[indexOfNew])
                        searchIntroduce.insert(addingIndex,searchIntroduceNew[indexOfNew])
                        searchAuther.insert(addingIndex,searchAutherNew[indexOfNew])
                        searchSite.insert(addingIndex,searchSite)
                    else:
                        searchBookNames.append(searchBookNamesNew[indexOfNew])#反之则加入至末尾并进行下一个
                        searchtezheng.append(searchtezhengNew[indexOfNew])
                        searchIntroduce.append(searchIntroduceNew[indexOfNew])
                        searchAuther.append(searchAutherNew[indexOfNew])
                        searchSite.append(searchSite)
    return searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchSite

def singleBookCrawl(booktezhengList,searchSiteList):
    mainSite=0
    (zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)=singleBookzhuyeCrawl(booktezhengList[mainSite],searchSiteList[mainSite])
    del zhuyeurl#删了省着报错
    bookInformationWrite(len(zhuyehtml_str),zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)
    startTime=datetime.datetime.now()
    print('Start getting data at '+startTime.strftime( '%H:%M:%S' ))
    for chapterIndex in range(len(zhuyehtml_str)):#遍历章节
        for workingIndex in range(len(booktezhengList)):
            workingSite=searchSiteList[workingIndex]#获取网站序号
            chapterContent=singleBookChapterCrawl(zhuyehtml_str[chapterIndex],booktezhengList[workingSite],workingSite)
            if chapterContent==True:#如果爬取成功
                print('\r'+'Completed: '+str(i)+'/'+str(len(zhuyehtml_str)-1), end='', flush=True)
                chapterContextHandle(chapterContent,zhuyeBookName,chapterName,chapterIndex)
                break#继续下一章
        else:#如果全部不成功
            chapterName=getChapterNameFromHtml(zhuyehtml_str[chapterIndex],workingSite)#正则抓取章节名
            print('Error: '+chapterName[0])
            with open(sys.path[0]+'\\'+zhuyeBookName+'\\'+zhuyeBookName+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
                f.write('')#创建总文件
            writejianjie('Error:'+str(i)+chapterName+'From\n',zhuyeBookName+'\\'+zhuyeBookName+'_总'+'.txt')#写入报错至总文件
            for i in range(len(searchSiteList)):
                errorWebsite=searchSiteList[i]
                writejianjie('  '+errorWebsite+'\n',zhuyeBookName+'\\'+zhuyeBookName+'_总'+'.txt')
            writejianjie('\n',zhuyeBookName+'\\'+zhuyeBookName+'_总'+'.txt')
    endTime=datetime.datetime.now()
    deltaTime=(endTime-startTime).seconds
    print('\n'+str(deltaTime)+' seconds'+'    '+str(deltaTime/len(zhuyehtml_str))+' seconds per chapter\n')

def singleBookzhuyeCrawl(tezheng,searchSite):
    if searchSite==0:#xsbiquge.com
        (zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)=paxsbqgzhuye(tezheng)
    elif searchSite==1:#booktxt.net
        (zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)=padingdianzhuye(tezheng)
    return zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction

def bookInformationWrite(chapterNum,bookName,bookAuther,bookIntroduction):
    print(bookName[0])
    print(str(chapterNum)+' in total')
    try:
        os.mkdir(bookName[0])#以书名创建文件夹
        print('Create folder: '+bookName[0])
    except:
        print('Folder with the same name: "'+bookName[0]+'" already exists')
    writejianjie('《'+bookName[0]+'》'+'\n',bookName[0]+'\\'+bookName[0]+'.txt')  #写入书籍相关信息至报告文件
    writejianjie('Auther: '+bookAuther[0]+'\n',bookName[0]+'\\'+bookName[0]+'.txt')
    writejianjie('    '+bookIntroduction[0]+'\n',bookName[0]+'\\'+bookName[0]+'.txt')
    writejianjie('Possible chapters: '+str(chapterNum)+'\n',bookName[0]+'\\'+bookName[0]+'.txt')
    with open(sys.path[0]+'\\'+bookName[0]+'\\'+bookName[0]+'_总'+'.txt','w',encoding='utf-8') as f:  #创建总文件
        f.write('')
    writejianjie('《'+bookName[0]+'》'+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')  #写入书籍相关信息至总文件
    writejianjie('Auther :'+bookAuther[0]+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')
    writejianjie('Possible chapters: '+str(chapterNum)+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')
    writejianjie('    '+bookIntroduction[0]+'\n',bookName[0]+'\\'+bookName[0]+'_总'+'.txt')
    return

def singleBookChapterCrawl(chapterHtml_str,tezheng,searchSite):#获取章节
    if searchSite==0:#xsbqg.com
        chapter=paxsbqgChapter(chapterHtml_str,tezheng)
    elif searchSite==1:#booktxt.net
        chapter=padingdianChapter(chapterHtml_str,tezheng)
    return chapter

def getChapterNameFromHtml(bookHtml,searchSite):#报错用
    if searchSite==0:#xsbiquge.com
        chapterName=re.findall('html">(.*?)</a></dd>',bookHtml,re.S)#正则抓取章节名
    elif searchSite==1:#booktxt.net
        chapterName=re.findall('html">(.*?)</a></dd>',bookHtml,re.S)#正则抓取章节名
    return(chapterName)

def chapterContextHandle(chapterContext,bookName,chapterName,chapterIndex):#写入文件
    if singleChapterOutPut==True:#是否输出单章
        with open(os.getcwd()+'\\'+bookName+'\\'+chapterName+'.txt','w',encoding='utf-8') as f:#创建f
            f.write(str(chapterIndex)+' '+chapterContext)#写入正文与节号至分文件
    writejianjie(str(chapterIndex)+' '+chapterName+'\n',bookName+'\\'+bookName+'_总'+'.txt')#写入章节名与节号至总文件
    writejianjie(chapterContext+'\n',bookName+'\\'+bookName+'_总'+'.txt')#写入正文至总文件

def siteIdToName(searchSite):
    siteName=''
    if searchSite==0:#xsbiquge.com
        siteName='xsbiquge.com'
    elif searchSite==1:#booktxt.net
        siteName='booktxt.net'
    return siteName

initialiseSettings()
while True:
    (keyWord)=getKeyWord()
    if '-' in keyWord:
        changeSettings(keyWord)
    else:
        (searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchSite)=getBookSearchingResult(keyWord)
        repetition=0
        printToSource={}
        for i in range(len(searchBookNames)):#遍历输出结果
            if i!=0 and searchBookNames[i]==searchBookNames[i-1]:#如果和存在重复则不输出
                repetition+=1
            else:
                print(str(i-repetition)+' '+searchBookNames[i])
                printToSource[i-repetition]=i
        (tezhengList,searchsiteList)=selectBook(searchBookNames,searchtezheng,searchIntroduce,searchAuther,searchSite,printToSource)
        #(zhuyeurl,zhuyehtml_str,zhuyeBookName,zhuyeBookAuther,zhuyeBookIntroduction)=singleBookzhuyeCrawl(tezheng[realIndex],searchSite[realIndex],mutiSource)
