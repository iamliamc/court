#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys, sqlite3, time
from bs4 import BeautifulSoup

print "We are in the right spot"

#Our source
gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
nmax = 900000

#Get Cookie
r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
headers = r.headers['set-cookie']
print headers

#Initialize opener add cookie
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', headers))
count_incompletes= open('exceptions.txt', 'w')

count = 1

localtime = time.localtime(time.time())

while count < nmax:
	print 'On Case #:', count
	#Request Page
	f = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(count))
	try: 
		bsoup = BeautifulSoup(f.read())
		#Storing the first b tag inside body to data_ccsort 
		data_ccsort = bsoup.body.b
	
		#If statement that sorts out civil cases 
		# if data_ccsort.string == u'Civil Case View':
			# print "Civil Case Continue..."
			# count +=1
			# print "ZZZZZZZ..."
			# time.sleep(1.8)
		if data_ccsort.string == 'Unable to load case data':
			print "Unable to load case data"
			count +=1
			time.sleep(1.8)
		else:
			criminal_out = open(str(count) +'.html', 'ab')
			criminal_out.write(str(bsoup))
			criminal_out.close()
			count += 1
			time.sleep(1.8)
	except:
		print "################ EXCEPTION #######################"
		time.sleep(120)
		count_incompletes.write(str(count))
		
		
		
		#### Do we want to REREQUEST AND CONTINUE? ####
		# r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
		# headers = r.headers['set-cookie']
		# #Initialize opener add cookie
		# opener = urllib2.build_opener()
		# opener.addheaders.append(('Cookie', headers))
		# continue

count_incompletes.close()
print "Start time:", localtime
print "End time:", time.localtime(time.time())

