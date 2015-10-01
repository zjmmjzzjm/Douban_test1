# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanMovieItem, DoubanTVItem
import json
import urllib
import urlparse
import sys


class DoubanTVSpider(scrapy.Spider):
	name = "douban_tv"
	allowed_domains = ["douban.com"]
	_step = 20 
	_cur_page = 0
	_cur_type = 0
	types = ['美剧',  '英剧',  '韩剧' , '日剧' , '国产剧' , '港剧' , '日本动画']
	start_urls = (
		'http://www.douban.com/',
	)
	params = {
			'type': 'tv',
			'tag' : '美剧',
			'sort': 'recommend',
			'page_limit': 20,
			'page_start': 0
			}
	url_parts = []
	

	def parse(self, response):
		tv_url = 'http://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=20&page_start=20'
		self.url_parts = list(urlparse.urlparse(tv_url))
		self.params['tag'] = self.types[0]
		self.params['page_start'] = 0
		self.url_parts[4] = urllib.urlencode(self.params)
		tv_url = urlparse.urlunparse(self.url_parts)
		print tv_url

		yield scrapy.Request(tv_url, callback=self.parse_tv)




	def parse_tv(self, response):
		data = json.loads(response.body)

		try:
			for i in data['subjects']: 
				item = DoubanTVItem()
				item['name'] = i['title']
				item ['rate'] = i['rate']
				yield item

		except Exception,e:
			print "Caught exception, " + str(e)
			self._cur_type += 1
			self._cur_page = 0
		else:
			if len(data['subjects']) == 0:
				self._cur_type += 1
				self._cur_page = 0
			else:
				self._cur_page += self._step

		if self._cur_type < len(self.types):
			self.params['tag'] = self.types[self._cur_type]
			self.params['page_start'] = self._cur_page 
			self.url_parts[4] = urllib.urlencode(self.params)
			tv_url = urlparse.urlunparse(self.url_parts)
			yield scrapy.Request(tv_url, callback=self.parse_tv)

