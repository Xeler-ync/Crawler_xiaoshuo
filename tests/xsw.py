#这是一段无用的代码，但是在未来可能会被重用

def paxswSearchPage(keyword):
    searchHtmlResult=requests.get('https://www.xiashuwu.com/search.html?searchkey='+keyword+'&searchtype=all').content.decode('utf-8')#请求搜索数据
    searchBookNames=re.findall('《<a href="/api/search/index/id/[0-9]+?/type/www/" target="_blank">(.*?)</a>》</h3></div>\n<div class="pic">\n<a href="/api/search/index/id/[0-9]+?/type/www/" target="_blank"><img ',searchHtmlResult,re.S)#正则抓取书名
    searchtezheng=re.findall('《<a href="/api/search/index/id/[0-9]+?/type/www/" target="_blank">.*?</a>》</h3></div>\n<div class="pic">\n<a href="/api/search/index/id/([0-9]+?)/type/www/" target="_blank"><img ',searchHtmlResult,re.S)#正则抓取网址
    searchIntroduce=re.findall('<div class="intro">&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>\n',searchHtmlResult,re.S)#正则抓取简介
    searchAuther=re.findall('<div class="nickname">(.*?) / 著</div>\n',searchHtmlResult,re.S)#正则抓取作者
    for i in range(len(searchtezheng)):#遍历输出结果
        print(str(i)+' '+searchBookNames[i])
    return (searchBookNames,searchtezheng,searchIntroduce,searchAuther)

def paxswzhuye(xiaoshuohao):#xiashuwu.com#未完成
    #下书网
    #https://www.xiashuwu.com/
    #傻逼华附
    #需要使用的库文件在外面
    #又是一个只能在家里做的东西
    #而且似乎在学校不一定能用
    #(searchBookNames,searchtezheng,searchIntroduce,searchAuther)=paxswSearchPage('霸道')
    #paxswzhuye(searchtezheng)
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

def paxswChapter(url,html_str,bookname,bookauther,bookintroduction,xiaoshuohao):#未完成
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
    with open(sys.path[0]+'\\'+bookname[0]+'\\'+bookname[0]+'_总'+'.txt','w',encoding='utf-8') as f:#创建f
        f.write('')#创建总文件
    writejianjie('《'+bookname[0]+'》'+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入书名至总文件
    writejianjie('Auther :'+bookauther[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入作者至总文件
    writejianjie('    '+bookintroduction[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入简介至总文件
    writejianjie('Possible chapters: '+str(len(html_str))+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入获取的章节数至总文件
    for i in range(len(html_str)):#遍历章节
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
            print('Error: Section'+i)
        else:
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
                print('Error: '+chapterName[0])
            text=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>',chapter,re.S)#正则抓取正文  #<div id="content">
            try:
                text[0]=text[0].replace('<br />&nbsp;','') #去除无用html标签
            except:#出错处理
                writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained'+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入出错章节
                writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'.txt')#写入源网址
                writejianjie('Section '+str(i)+'('+chapterName[0]+')has an error and cannot be obtained''\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入总文件
                writejianjie('Source address: '+chapterUrl+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入源网址
                print('Error: '+chapterName[0])
            else :
                    text[0]=text[0].replace('&nbsp;','')#去除无用html标签
                    text[0]=text[0].replace('&amp;nbsp;','')#去除无用html标签
                    text[0]=text[0].replace('<br />','\n')#处理换行
                    with open(sys.path[0]+'\\'+bookname[0]+'\\'+chapterName[0]+'.txt','w',encoding='utf-8') as f:#创建f
                        f.write(str(i)+' '+text[0])#写入正文与节号至分文件
                    writejianjie(str(i)+' '+chapterName[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入章节名与节号至总文件
                    writejianjie(text[0]+'\n',bookname[0]+'\\'+bookname[0]+'_总'+'.txt')#写入正文至总文件
                    print('Completed: '+str(i)+' '+chapterName[0])

#这是一段无用的代码，但是在未来可能会被重用