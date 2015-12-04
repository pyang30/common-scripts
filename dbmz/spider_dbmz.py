__author__ = 'yph'

import urllib
import urllib2
import re
from HTMLParser import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import cookielib
from time import sleep

#path to store the pictures
pic_dir = r'C:\dbmz'

page_pics = 0
total_pics = 0

enable_proxy = True
proxy_handler = urllib2.ProxyHandler({"http":"http://proxy02.cd.intel.com:911"})
null_proxy_handler = urllib2.ProxyHandler({})


user_agent = r'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent}
cj = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cj)

handler = (proxy_handler, handler)
opener = urllib2.build_opener(*handler)
urllib2.install_opener(opener)

def get_url_srouce(url):
    try:
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)

        resp = response.read()
        return resp

    except urllib2.URLError, e:
        print(e.reason)
        return ""

def download_pic(url, filename):
    with open(filename, 'wb') as f:
        f.write(urllib2.urlopen(url).read())

def count_pics():
    global total_pics, page_pics
    total_pics += 1
    page_pics += 1

class PicParser(HTMLParser, object):
    def __init__(self):
        self.parse = False
        super(PicParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and 'class' in dict(attrs).keys() \
            and dict(attrs)['class'] == 'topic-figure cc':
            self.parse = True

        if tag == 'img' and self.parse == True:
            key_dict = dict(attrs)
            target_key = ['class', 'alt', 'src']
            if set(target_key).issubset(set(key_dict.keys())):
                pic_url = key_dict['src']
                # print(pic_url)

                filename = os.path.basename(pic_url)
                print("Downloading %s ... " % filename)
                path = pic_dir + os.path.sep + filename

                if not os.path.exists(path):
                    try:
                        download_pic(pic_url, path)
                        sleep(1.5)
                    except Exception, e:
                        print "download error ", e.args
                else:
                    print("%s already exists ..." % filename)

                count_pics()
                self.parse = False



class PageParser(HTMLParser, object):
    def __init__(self):
        target_key = ['class', 'title', 'href']
        self.target_set = set(target_key)
        super(PageParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            key_dict = dict(attrs)
            # print(key_dict)
            if self.target_set.issubset(set(key_dict)):
                src_url = key_dict['href']
                # print 'parser ', src_url
                try:
                    PicParser().feed(get_url_srouce(src_url))
                    sleep(1.5)
                except:
                    print("Error %s" % src_url)


def download_thread(url):
    data = get_url_srouce(url)
    # print(data)
    if data == "":
        sys.exit()
    PageParser().feed(data)


if __name__ == "__main__":
    if not os.path.exists(pic_dir):
        os.mkdir(pic_dir)

    for page in range(0, 4000, 5):
        print("go to page %d" % page)
        url = "http://www.douban.com/group/meituikong/discussion?start=" + str(page)
        download_thread(url)
        print("in page %d, got %s pics, totally got %s pics" % (page, page_pics, total_pics))
        page_pics = 0
        sleep(3)
