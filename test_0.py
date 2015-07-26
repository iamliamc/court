import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys, sqlite3, time
from bs4 import BeautifulSoup

##1529 in size_0.txt

f = open("size_0.txt")

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

empty = 0
not_empty = 0
problem = 0
me = []

with f as fp:
	for line in fp:
		line = line.replace("DataMob/", "")
		line = line.replace(".html", "")
		z = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(line))
		try: 
			bsoup = BeautifulSoup(z.read())
			data_ccsort = bsoup.body.b
			if (data_ccsort.string == u'Civil Case View') or (data_ccsort.string == 'Unable to load case data'):
				print "Civil Case Continue..."
				empty +=1
				print "ZZZZZZZ..."
			else:
				not_empty +=1
				me.append(line)
		except:
			problem += 1
print "NUM CIVL %s" % empty
print "NUM NOT CIVIL %s" % not_empty
print "NUM NOT GOOD %s" % problem
print me
