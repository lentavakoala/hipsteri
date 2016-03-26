import sys
import time
import random
import datetime
import telepot
import sys
import urllib
import os
import glob
import time
from bs4 import BeautifulSoup
import requests
import re
import urllib2
from xml.dom import minidom

wurl = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
wser = 'http://xml.weather.yahoo.com/ns/rss/1.0'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def lueApiKey():
	key = [line.rstrip('\n') for line in open('./apiKey.txt')]
	return key[0]

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def get_soup(url,header):
	return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

def haeKuva():
	image_type = "Action"
	query = "oispa kaljaa"
	query= query.split()
	query='+'.join(query)
	url=url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)
	images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
	kuva = random.randint(1,len(images)-1)
	kuvatus = raw_img = urllib2.urlopen(images[kuva]).read()
	DIR = './'
	f = open(DIR + image_type + "temp.jpg", 'wb')
	f.write(raw_img)
	f.close()

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		lampo = float(temp_string) / 1000.0
        return lampo

def seppo():
	data = [line.strip() for line in open("./seppo.txt", 'r')]
	satunnainen = random.randint(1,len(data)) 
	quote = data[satunnainen-1]
	return quote

def matti():
        data = [line.strip() for line in open("./matti.txt", 'r')]
        satunnainen = random.randint(1,len(data))
        quote = data[satunnainen-1]
        return quote


def weather_for_zip(zip_code):
	url = wurl % zip_code +'&u=c'
	dom = minidom.parse(urllib.urlopen(url))
	forecasts = []
	for node in dom.getElementsByTagNameNS(wser, 'forecast'):
        	forecasts.append({
           	 'date': node.getAttribute('date'),
            	'low': node.getAttribute('low'),
            	'high': node.getAttribute('high'),
            	'condition': node.getAttribute('text')
        	})
	ycondition = dom.getElementsByTagNameNS(wser, 'condition')[0]
	return {'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'forecasts': forecasts ,
        'title': dom.getElementsByTagName('title')[0].firstChild.data
	}

def saa(kaupunki):
	a=weather_for_zip("GMXX0007")
	response =  '==================================\n'
	response += '       Berlin, Germany\n'
	response += '==================================\n'
 	response += 'current condition= '+a['current_condition']+'\n'
 	response += 'current temp     = '+a['current_temp']+'\n'
 	response += '=================================='+'\n'
	response += '  today     ='+a['forecasts'][0]['date']+'\n'
	response += '  hight     ='+a['forecasts'][0]['high']+'\n'
	response += '  low       ='+a['forecasts'][0]['low']+'\n'
	response += '  condition ='+a['forecasts'][0]['condition']+'\n'
	response += '=================================='+'\n'
	response += '  tomorrow  ='+a['forecasts'][1]['date']+'\n'
	response += '  hight     ='+a['forecasts'][1]['high']+'\n'
	response += '  low       ='+a['forecasts'][1]['low']+'\n'
 	response += '  condition ='+a['forecasts'][1]['condition']+'\n'
	response += '=================================='+'\n'
	return response

def reagoiKuvaan():
	reaktio = ['Prost, %s!']
	arpa = random.randint(1,len(reaktio))
	return reaktio[arpa-1]

def kehitaKakkulause():
        kakkulinkki = [line.strip() for line in open("./reseptit.txt", 'r')]
	arpa = random.randint(1,len(kakkulinkki))

	jorina = [line.strip() for line in open("./jorina.txt", 'r')]
	
	joriarpa = random.randint(1,len(jorina))

	kakkustringi = jorina[joriarpa-1]+kakkulinkki[arpa-1]

	return kakkustringi


def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	chat_id = msg['chat']['id']
	if content_type == 'text':
		print msg
		command = msg['text'].encode("utf-8")
		print 'Mua komennettiin :( : %s' % command
		print 'Kanavan ID: %s' % chat_id
		if command == '/kakku':
    			bot.sendMessage(chat_id, kehitaKakkulause())
		elif 'seppo' in command:
			bot.sendMessage(chat_id, seppo())
		elif 'Seppo' in command:
			bot.sendMessage(chat_id, seppo())
		elif 'masa' in command:
			bot.sendMessage(chat_id, matti())
		elif 'Masa' in command:
			bot.sendMessage(chat_id, matti())
		elif 'kakku' in command:
    			bot.sendMessage(chat_id, kehitaKakkulause())
		elif 'Raakakakku' in command:
			bot.sendMessage(chat_id, kehitaKakkulause())
		#elif 'kalja' in command:
#		bot.sendMessage(chat_id, 'Kalja mainittu! Prost!')
		#	pass
		elif 'oispa kaljaa' in command:
			haeKuva()
			f = open('Actiontemp.jpg', 'rb')
			bot.sendPhoto(chat_id, f)
		elif 'luukku' in command:
			bot.sendMessage(chat_id, 'Villen lukaalissa on mukavat '+str(read_temp()) +'C')
		elif 'mauerpark' in command:
			bot.sendMessage(chat_id, 'Ah, Mauerpark! Bertsassa on parhaat kirpparit')
		elif command == 'weather':
			bot.sendMessage(chat_id, saa('Berlin'))
	if content_type == 'photo':
		bot.sendMessage(chat_id, reagoiKuvaan() % msg['from']['first_name'])

avain = lueApiKey()
bot = telepot.Bot(avain)
bot.notifyOnMessage(handle)
print 'Kuulolla ollaan ...'

while 1:
    time.sleep(10)
