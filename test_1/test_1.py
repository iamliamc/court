import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys, sqlite3, time
from bs4 import BeautifulSoup

##1529 in size_0.txt

# gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
# nmax = 925100
# nmax2 = 25000

# #Get Cookie
# r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
# headers = r.headers['set-cookie']
# print headers

# #Initialize opener add cookie
# opener = urllib2.build_opener()
# opener.addheaders.append(('Cookie', headers))


count = 1
missing = []

# while count < 100000:
	# for filename in os.listdir('D:\grcourt-master\DataMob'):
			# filename = filename.replace("DataMob/", "")
			# filename = filename.replace(".html", "")
			# if (filename != count):
				# print filename
				# z = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(filename))
				# try: 
					# bsoup = BeautifulSoup(z.read())
					# data_ccsort = bsoup.body.b
					# if (data_ccsort.string == u'Civil Case View') or (data_ccsort.string == 'Unable to load case data'):
						# print "Civil Case Continue... or Unable to load case data"
						# count += 1					
					# else:
						# criminal_out = open(str(count) +'.html', 'ab')
						# criminal_out.write(str(bsoup))
						# count += 1
						# missing.append(filename)
				# except:
					# criminal_out = open(str(count) +'.html', 'ab')
					# criminal_out.write(str(bsoup))
					# missing.append(filename)
					# count += 1
			# else:
				# count += 1

				
for filename in os.listdir('D:\grcourt-master\DataMob'):
	count += 1
	missing.append(int(filename.replace(".html", "")))
	print '%s' % count

print "Starting sort"
x = missing.sort()
missing == x
print "Print Missing to File"		
thefile = open("sorted_results.txt", 'w')

for item in missing:
  thefile.write("%s\n" % item)