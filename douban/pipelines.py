# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from douban.items import DoubanMovieItem, DoubanTVItem

class DoubanPipeline(object):
	def process_item(self, item, spider):
		if isinstance(item ,DoubanMovieItem):
			with open("movies.txt", "a") as f:
				f.write('%s,\t%s\n' % (item['name'].encode('utf8'), item['desc'].encode('utf8')))
		elif isinstance(item , DoubanTVItem):
			print "-------->is douban ", type(item)
			with open("tvs.txt", "a") as f:
				f.write('%s,\t%s\n' % (item['name'].encode('utf8'), item['rate'].encode('utf8')))
	
		return item
