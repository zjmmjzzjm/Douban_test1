# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):
	def process_item(self, item, spider):
		with open("movies.txt", "a") as f:
			f.write('%s,\t%s\n' % (item['name'].encode('utf8'), item['desc'].encode('utf8')))
		return item
