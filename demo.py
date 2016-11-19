# -*- coding: utf-8 -*-
# @Date    : 2016/11/16  19:39
# @Author  : 490949611@qq.com

from PIL import Image
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys

def getHostPic1(roomid):
	url = 'http://www.panda.tv/'+str(roomid)
	cap = webdriver.DesiredCapabilities.PHANTOMJS
	cap["phantomjs.page.settings.resourceTimeout"] = 1000
	driver = webdriver.PhantomJS(desired_capabilities=cap)
	driver.get(url)
	# assert 'pandaTV' in driver.title
	code = driver.page_source
	# r = requests.get(url)
	# print unicode(r.text)
	soup = BeautifulSoup(code)
	try:
		print 'roomid===',roomid
		imgs = soup.find('div',attrs={'class':'room-detail-intro'})
		if imgs:
			imgs = imgs.find_all('img')
			i = 1
			for img in imgs:
				if 'jpeg' in img['src']:
					filename = '%s-%d.jpeg' % (str(roomid),i)
					saveImage(img['src'],filename)
				i += 1
		else:
			print 'no picture!!!'
			pass
	except Exception,e:
		print str(e)
		pass
	# driver.get('https://www.baidu.com')
	# elem = driver.find_element_by_class_name('s-text-content').text
	# print elem
	# html = driver.page_source
	# soup = BeautifulSoup(html,'lxml')
	# print soup

def saveImage( imgUrl,imgName ="default.jpg" ):
	response = requests.get(imgUrl, stream=True)
	image = response.content
	DstDir="F:\\pandaHost\\"
	print(u"保存文件"+DstDir+imgName+"\n")
	try:
		with open(DstDir+imgName ,"wb") as jpg:
			jpg.write(image)
			return
	except IOError:
		print("IO Error\n")
		return
	finally:
		jpg.close


def getVideoList():
	roomidList = []
	url = 'http://www.panda.tv/cate/yzdr'
	r = requests.get(url)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text,"lxml")
	result_all = soup.find('ul',attrs={"id":'sortdetail-container'}).find_all('li')
	print type(result_all)
	for item in result_all[:40]:
		roomid = item['data-id']
		# title = item.find('div',attrs={'class':'video-title'})['title']
		# name = item.find('div',attrs={'class':'video-info'}).find_all('span')[0].string
		# roomnum = item.find('div',attrs={'class':'video-info'}).find_all('span')[1].string
		# print  u'房间名：',unicode(title),u'主播名:',unicode(name),u'房间号:',roomid
		roomidList.append(roomid)
	return roomidList

def rankOfGift():
	params={
		# 'token':'0605444305e4b1da3cacdc302b02012',
		'anchor_id':'5290260',#主播的id！
		# '_':time.time()
	}
	url='http://rank.service.panda.tv/weekly'#room_total
	r = requests.get(url,params=params)
	r.encoding = 'utf-8'
	response_all = r.json()
	for item in response_all:
		nickname = item['nickname']
		print nickname


if __name__ == '__main__':
	roomidList = getVideoList()
	for i in range(0,len(roomidList)):
		getHostPic1(roomidList[i])
	# getHostPic1(35723)
	# print 'download over!'
	# getBulletScreen(888888)
	# getHostPic1(441602)
	# getBulletScreen(6666)
