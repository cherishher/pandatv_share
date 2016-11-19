#熊猫TV视频及弹幕爬虫介绍
##爬虫介绍
网络爬虫，是一种自动获取网页内容的程序。是搜索引擎的重要组成部分，因此搜索引擎优化很大程度上就是针对爬虫而做出的优化。  

[如何入门python爬虫](https://www.zhihu.com/question/20899988)
##python爬虫需要的库
- urllib
- urllib2
- **requests** [参考文档](http://www.python-requests.org/en/master/)
- **bs4** [参考文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#)
- **selenium**
- scrapy
- pyspider

##需要掌握什么？
- python基础
- http协议（get，post请求）
- 包结构
- html，css，js基础
- cookie的应用
- 。。。
##HTTP
![](http://www.runoob.com/wp-content/uploads/2013/11/httpmessage.jpg)

##requests
###发送请求：
- requests.get(url[,data[,headers[,cookies]]])  
- requests.post(url[,data[,headers[,cookies]]])
###返回数据：
    r = requests.post()
    r.text
    r.content
    r.json()
    r.status_code
    r.headers
	r.encoding
    。。。
###实例
    >>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))  
    >>> r.status_code  
    200  
    >>> r.headers['content-type']
    'application/json; charset=utf8'
    >>> r.encoding
    'utf-8'
    >>> r.text
    u'{"type":"User"...'
    >>> r.json()
    {u'private_gists': 419, u'total_private_repos': 77, ...}
##BeautifulSoup
###调用方法：
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc)
###返回数据：
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:  
- **Tag**  
- NavigableString  
- **BeautifulSoup**  
- Comment
###实例：
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
    tag = soup.b
    type(tag)
    # <class 'bs4.element.Tag'>
    tag['class']
    # u'boldest'
    tag.string
    # u'Extremely bold'
##进入PandaTV

