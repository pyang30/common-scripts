import urllib
import urllib2
import json

url = u"http://tubu.ibuzhai.com/rest/v2/travelog/4736"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"

def get_item_pics(item):
	sub_url = item_url + item['id']
	print sub_url
	res = urllib2.urlopen(sub_url)
	

if __name__ == "__main__":
	results = []	

	res = urllib2.urlopen(url)
	data = res.read()
	print data
	#data = json.loads(data)
	#print data["log"]
