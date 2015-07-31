#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys, sqlite3, time
from bs4 import BeautifulSoup

print "We are in the right spot"
os.system("del criminal_out.csv")

#Our source
gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
nmax = 925100
nmax2 = 25000

#Get Cookie
r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
headers = r.headers['set-cookie']
print headers

#Initialize opener add cookie
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', headers))
count_incompletes= open('workfile.txt', 'w')

count = 1

localtime = time.localtime(time.time())

while count < nmax2:
	print 'On Case #:', count
	#Request Page
	f = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(count))
	try: 
		bsoup = BeautifulSoup(f.read())
		#global problems
		#problems = []
		#Storing the first b tag inside body to data_ccsort 
		data_ccsort = bsoup.body.b
	
		#If statement that sorts out civil cases 
		if data_ccsort.string == u'Civil Case View':
			print "Civil Case Continue..."
			count +=1
			print "ZZZZZZZ..."
			time.sleep(1.5)
		elif data_ccsort.string == 'Unable to load case data':
			print "Unable to load case data"
			count +=1
			print "ZZZZZZZ..."
			time.sleep(1.5)
		else:
			print "Criminal Case"
			criminal_out = open(str(count) +'.html', 'ab')
			criminal_out.write(str(bsoup))
			
			count += 1
			print count
			criminal_out.close()
			time.sleep(1.5)
	except:
		print "################ EXCEPTION #######################"
		time.sleep(5)
		count_incompletes.write(str(count) + ' ,')
		r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
		headers = r.headers['set-cookie']
print headers

#Initialize opener add cookie
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', headers))
		continue
		
#print problems, "Problem child?"
localtime_end = time.localtime(time.time())
count_incompletes.close()
print "Start time:", localtime
print "End time:", localtime_end

