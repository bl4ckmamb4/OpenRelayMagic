import time
import json, requests
import socket
import smtplib
import random, string
import argparse
from tqdm import *
from multiprocessing import Pool
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
socket.setdefaulttimeout(15)

def randomshit():
	digits = "".join( [random.choice(string.digits) for i in range(5)] )
	chars = "".join( [random.choice(string.ascii_letters) for i in range(5)] )
	randomtext = (chars+digits)
	return randomtext

def checker(hostname):
	socket.setdefaulttimeout(15)
	try:
		sender = 'newsletter@'+hostname
		receiver = 'dracarys@getnada.com'
		rando = randomshit()
		subject = ('Unique identify '+rando)
		messageHTML = '<h1>lets test this sh1t</h1><p>Visit <a href="https://mybitch.net/">mybitch.net<a> for some great <span style="color:#000000">qwertybitch</span><p>'
		messagePlain = 'Mod this if you want to send a plain message'
		msg = MIMEMultipart('alternative')
		msg['From'] = sender
		msg['To'] = receiver
		msg['Subject'] = subject
		msg.attach(MIMEText(messageHTML, 'html'))
		if args.port == 465:
			port = 465
			server = smtplib.SMTP_SSL(hostname, port)
		else:
			port = 587
			server = smtplib.SMTP(hostname, port)
		server.helo()
		text = msg.as_string()
		server.sendmail(sender, receiver, text)
		server.quit()

		time.sleep(15)
		check_url = "https://getnada.com:443/api/v1/inboxes/dracarys@getnada.com"
		check_cookies = {"tarteaucitron": "!adsense=true!gajs=true", "__gads": "Test", "__utmt": "1"}
		check_headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Referer": "https://getnada.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
		rr = requests.get(check_url, headers=check_headers, cookies=check_cookies, verify=False, timeout=30)
		json_data = json.loads(rr.text)
		msgs = json_data['msgs']
		delete_key = ''
		for i in msgs:
			if rando in str(i):
				if args.output:
					formatted = ('Vulnerable: ',hostname,port)
					f=open(args.output,'a')
					f.write(str(formatted)+'\n')
					f.close()
				else:
					print ('Vulnerable Host:',hostname,'Port:',port)
				delete_key = (i['uid'])
				#time.sleep(2)
				delete_cookies = {"tarteaucitron": "!adsense=true!gajs=true", "__gads": "Test", "__utmt": "1"}
				delete_url = ("https://getnada.com:443/api/v1/messages/"+str(delete_key))
				delete_headers = {"Connection": "close", "Origin": "https://getnada.com", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "same-origin", "Referer": "https://getnada.com/msg", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
				requests.delete(delete_url, headers=delete_headers, cookies=delete_cookies, verify=False, timeout=30)
			else:
				None
	except:
		None

if __name__ == '__main__':
	print ('''
 _  _  _  _  _ _ | _    _ _  _  _ . _
(_)|_)(/_| || (/_|(_|\/| | |(_|(_||(_
   |                 /          _|   
       -- keep em closed --
''')
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--list", help="Domain List")
	parser.add_argument("-t", "--target", help="Single Host")
	parser.add_argument("-p", "--port", help="Define 465/587")
	parser.add_argument("-o", "--output", help="Output of Results")
	parser.add_argument("-T", "--threads", help="No. of threads", default=10, type=int)
	args = parser.parse_args()
	if args.target:
		checker(args.target)
	elif args.list:
		lineList = [line.rstrip('\n') for line in open(args.list)]
		processcount = args.threads
		with Pool(processes=processcount) as p:
			if args.output:
				max_ = (len(lineList))
				with tqdm(total=max_) as pbar:
					for i, _ in tqdm(enumerate(p.imap_unordered(checker, lineList))):
						pbar.update()
				print('\n')
			else:
				p.map(checker, lineList)
				print('\n')
