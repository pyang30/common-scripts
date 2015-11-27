# -*- coding:utf-8 -*- 
import mimetypes
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr,formataddr
import smtplib
import os
import sys;
reload(sys);
sys.setdefaultencoding("utf8")


smtp_server = "smtp.qiye.163.com"
helo = "smtp.qiye.163.com"
smtp_port = 25

class Mail(object):
	def __init__(self, argv):
		#print argv
		self.to_user = argv[0]
		self.subject = argv[1]
		self.file = argv[2]
		self.from_user = argv[3]
		self.passwd = argv[4]
		
		self.content = ""
		if os.path.exists(self.file):
			self.content = open(self.file).read()
		else:
			self.content = self.file
		#print self.content	
		self.msg = None
		
		self.arg_len = len(argv)
		
		if self.arg_len != 5:
			self.show_help()
		

	def gen_msg(self, subject, content, to_user, from_user):
		print "mail"
		msg = MIMEText(content, "html", "utf-8")
		msg['Subject'] = subject
		msg['From'] = from_user
		msg['to'] = to_user
		return msg
		
	def send_msg(self):
		if self.arg_len != 5:
			self.show_help()
			pass
			
		self.msg = self.gen_msg(self.subject, self.content, self.to_user, self.from_user)
		try:
			server = smtplib.SMTP(smtp_server, smtp_port)
			server.login(self.from_user, self.passwd)
			to_list = self.to_user.split(',')
			server.sendmail(self.from_user, to_list, self.msg.as_string())
			server.quit()
			print "send successfully"

		except Exception, e:
			print str(e)
			print "send failed"

	def show_help(self):
		err_code_map = {
				0:"ERR_NO_MAIL_RECIPIENTS",
				1:"ERR_NO_MAIL_SUBJECT",
				2:"ERR_NO_MAIL_BODY",
				3:"ERR_NO_SMTP_USER",
				4:"ERR_NO_SMTP_PASSWORD"
				}

		err_code = "ERR_NOT_ENOUGH_ARGUMENTS"
		print ""
		print err_code," : ", err_code_map[length-1]
		print "Usage: python %s recipients subject content user userpwd" % __file__
		

class PicMail(Mail):
	def __init__(self, argv):
		super(PicMail, self).__init__(argv)

	def gen_msg(self, subject, content, to_user, from_user):
		#msg = MIMEText(content, "html", "utf-8")
		print "picmail"
		msg = MIMEMultipart("alternative")
		msg['Subject'] = subject
		msg['From'] = from_user
		msg['to'] = to_user
		html = """\
		<html>
		<body>
		"""
		html += "</br>"
		html += content
		html += "</br>"
		html += "</br>"
		html += """
		<img src="cid:img1"></br>
		<img src="cid:img2"></br>
		<img src="cid:img3"></br>
		<img src="cid:img4"></br>
		<img src="cid:img5"></br>
		<img src="cid:img6"></br>
		</body>
		</html>'
		"""
		content = MIMEText(html, "html", "utf-8")
		msg.attach(content)
		
		files = ["bgpa.png", "bgpb.png", "bgpc.png", "gds.png", "js.png", "hk.png"]
		imgs = ["img1", "img2", "img3", "img4", "img5", "img6"]
		maps = dict(zip(files, imgs))
		for f in maps.keys():
			fp = open(f,"rb")
			msgImage = MIMEImage(fp.read())
			fp.close
			msgImage.add_header("Content-ID", maps[f])
			msg.attach(msgImage)
		return msg		
	
		
if __name__ == '__main__':
	#print sys.argv
	if len(sys.argv) != 6:
		print "Usage: python %s recipients subject content user userpwd" % __file__
		sys.exit(0)

	mail = Mail(sys.argv[1:])
	mail.send_msg()
