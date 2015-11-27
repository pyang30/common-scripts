import urllib
import urllib2
import json
import thread
import threading

url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=2000"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"
travels = []

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global get_item_pics
		get_item_pics(self.item)	

if __name__ == "__main__":
	results = []	

	res = urllib2.urlopen(url)
	data = res.read()
    #print data
	data = json.loads(data) 
	data_list = data['logs']

	for item in data_list:
		content = {}
		temp = []
		content["id"] = item["id"]
		content["pics"] = temp
		results.append(content)	

	print len(results)
	for item in results:
		id = item['id']
		print id
		travels.append(item_url + item['id'])

	print travels	
	with open("travel_log.txt", 'w') as f:
		for item in travels:
			f.write(item+'\n')	
