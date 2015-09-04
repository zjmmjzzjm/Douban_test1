# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanMovieItem


class DoubanMovieSpider(scrapy.Spider):
	name = "douban_movie"
	allowed_domains = ["douban.com"]
	year = 1899
	start = 0
	_step = 15

	start_urls = (
		'http://www.douban.com/',
	)

	def parse(self, response):
		movie_url = "http://www.douban.com/tag/%d/movie?start=%d"%(self.year, self.start)
		yield scrapy.Request(movie_url, callback=self.parse_movie)




	def parse_movie(self, response):
		movie_list = response.xpath('//dl')
	
		if len(movie_list) == 0:
			if self.year < 2015:
				self.year += 1
				self.start = 0
			else:
				import sys
				sys.exit()
		else :
			self.start += self._step


		try:
			for i in movie_list: 
				#print i.xpath('dd/a/text()').extract()[0].strip()
				#print i.xpath('dd/div[@class="desc"]/text()').extract()[0].strip()
				#i.xpath('dd/a/text()').extract()[0]
				#i.xpath('dd/div[@class="desc"]/text()').extract()[0].strip()
				item = DoubanMovieItem()
				item['name'] = i.xpath('dd/a/text()').extract()[0]
				item['desc'] = i.xpath('dd/div[@class="desc"]/text()').extract()[0].strip()
				yield item

		except Exception,e:
			print "Caught exception, " + str(e)

		movie_url = "http://www.douban.com/tag/%d/movie?start=%d"%(self.year,self.start)
		yield scrapy.Request(movie_url, callback=self.parse_movie)

