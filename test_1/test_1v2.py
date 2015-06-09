import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys, sqlite3, time
from bs4 import BeautifulSoup

##1529 in size_0.txt

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

myfile = open("spottedResults.txt")
count = 1
missing = []
last_filename = 0

while count < 100000:
	with myfile as f:
		for filename in f:
			current_file = int(filename)
			print "FILENAME %d", filename
			print "LAST_FILENAME %d", last_filename
			if filename != (last_filename + 1):
				for x in range(last_filename, (current_file + 1)):
					print "Sorted File: ", x
					try: 
						z = opener.open("http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1" + str(x))
						bsoup = BeautifulSoup(z.read())
						data_ccsort = bsoup.body.b
						if (data_ccsort.string == u'Civil Case View') or (data_ccsort.string == u'Unable to load case data'):
							print "Civil Case Continue... or Unable to load case data"
							continue
						else:
							criminal_out = open(str(x) +'.html', 'ab')
							criminal_out.write(str(bsoup))
							missing.append(filename)
							
					except:
						criminal_out = open(str(x) +'.html', 'ab')
						criminal_out.write(str(bsoup))
						missing.append(filename)
					print "LAST FILENAME BEFORE %s" % last_filename
					last_filename = x
					print "LAST FILENAME AFTER %s" % last_filename
					count += 1
			else:
				continue
				
# for filename in os.listdir('D:\grcourt-master\DataMob'):
	# count += 1
	# missing.append(int(filename.replace(".html", "")))
	# print '%s' % count

# print "Starting sort"
# x = missing.sort()
# missing == x
# print "Print Missing to File"		
# thefile = open("sorted_results.txt", 'w')

# for item in missing:
  # thefile.write("%s\n" % item)