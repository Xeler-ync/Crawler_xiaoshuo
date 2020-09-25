import selenium
#从selenium里面导入webdriver
from selenium import webdriver

#指定chrom的驱动
#执行到这里的时候Selenium会到指定的路径将chrome driver程序运行起来
driver = webdriver.Edge('C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\Python37_64\\Scripts\\msedgedriver.exe')
#driver = webdriver.Firefox()#这里是火狐的浏览器运行方法

#get 方法 打开指定网址
driver.get('www.baidu.com')

#选择网页元素
element_keyword = driver.find_element_by_id('kw')

#输入字符
element_keyword.send_keys('宋曲')

#找到搜索按钮
element_search_button = driver.find_element_by_id('su')


#傻逼华附操你妈
#https://www.jianshu.com/p/1b63c5f3c98e
#https://blog.csdn.net/weixin_42551465/article/details/80817552