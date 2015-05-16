#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys
from bs4 import BeautifulSoup

#Move to Work
#os.chdir("C:\Users\TPB\Desktop\scrape")
print "We are in the right spot"
os.system("del criminal_out.csv")

#Our source
gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
nmax = 891429

#High Count
#Main while loop with Crawler calls parse_gr Choose a different page each run
count = random.randint(1,100000)
#count = 43023

#Multiple Bonds:
#count = 42976 

#Get Cookie
r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
headers = r.headers['set-cookie']
print headers

#Initialize opener add cookie
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', headers))

def stable_table(regex_return, sec_list):		
	for item in regex_return:
		table_soup = BeautifulSoup(item)
		for x in table_soup.find_all(class_="medium"):
			for td_tag in x.find_all("td"):
				#print td_tag
				sec_list.append(str(td_tag.get_text(strip=True)))
		return sec_list

def stable_table_address(regex_return, sec_list):		
	for item in regex_return:
		table_soup = BeautifulSoup(item)
		for x in table_soup.find_all(class_="medium"):
		#Replace <br> tag with space
			x = str(x).replace('<br>', ' ')
			x = BeautifulSoup(x)
			for td_tag in x.find_all("td"):
				sec_list.append(str(td_tag.get_text(strip=True)))
		return sec_list		
		
		
def handle_mult(section_inf, next_list, fields):
	numb = int(len(section_inf)/fields)
	s_index = 0
	e_index = fields
	next_list = []
	for case in range(numb):
		next_list.append(tuple(section_inf[s_index:e_index]))
		s_index += fields
		e_index += fields
	return next_list

def handle_mult(section_inf, next_list, fields):
	numb = int(len(section_inf)/fields)
	s_index = 0
	e_index = fields
	next_list = []
	for case in range(numb):
		next_list.append(tuple(section_inf[s_index:e_index]))
		s_index += fields
		e_index += fields
	return next_list	

#Regular Expressions for Splitting Page By Comments Storing Results in Variables:
#<!-- DEFENDANT --> == sec_defendant
#<!-- CHARGES -->  == sec_charges
#<!-- SENTENCE --> == sec_sentence
#<!-- BONDS --> == sec_bonds
#<!-- Register of Actions --> sec_roa
#<!-- Case History --> sec_casehist

criminal_out = open("criminal_out.csv", 'ab')
with criminal_out as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(["Defendant", "Case Number", "Language", "Mailing Address", "Race", "Sex", "Height", "DOB", "Weight", "Hair", "Eyes", "Attorney", "Firm", "Attorney Phone", "Judge", "OffenseDate", "DateClosed", "OffenseDescription", "Disposition", "DispositionDate", "Fines", "Jail Days", "Probation", "Balance Due", "Bench Warrant Issued", "DateIssued", "Type", "Amount", "PostedDate"])


index_2 = 1
#Define main parse HTML function
def parse_gr(bsoup):
	data_medium = bsoup.find_all(class_="medium")
	data_XLheader = bsoup.find_all(class_="extralarge")
	data_ccsort = soup.body.b
	print data_ccsort.string
	global problems
	
	#def_list fields ["Defendant", "Case Number", "Language", "Mailing Address", "Race", "Sex", "Height", "DOB", "Weight", "Hair", "Eyes", "Attorney", "Firm", "Attorney Phone", "Judge"]
	def_list = []
	regex_defendant = re.compile(r'.*<!-- DEFENDANT -->(.*)<!-- CHARGES -->.*', re.DOTALL)
	sec_defendant = regex_defendant.findall(str(bsoup))

	
	#charge_list fields ["OffenseDate1", "Date Closed1", "Offense Description"1, Disposition"1, "Disposition Date1", OffenseDate2..."]
	charge_list = []
	regex_charges = re.compile(r'.*<!-- CHARGES -->(.*)<!-- SENTENCE -->.*', re.DOTALL)
	sec_charges = regex_charges.findall(str(bsoup))
	
	sen_list = []
	regex_sentence = re.compile(r'.*<!-- SENTENCE -->(.*)<!-- BONDS -->.*', re.DOTALL)
	sec_sentence = regex_sentence.findall(str(bsoup))
	
	bonds_list = []
	regex_bonds = re.compile(r'.*<!-- BONDS -->(.*)<!-- Register of Actions -->.*', re.DOTALL)
	sec_bonds = regex_bonds.findall(str(bsoup))
	
	roa_list = []
	regex_roa = re.compile(r'.*<!-- Register of Actions -->(.*)<!-- Case History -->.*', re.DOTALL)
	sec_roa = regex_roa.findall(str(bsoup))
	
	case_list = []
	regex_casehist = re.compile(r'.*<!-- Case History -->(.*)<!-- END Main -->.*', re.DOTALL)
	sec_casehist = regex_casehist.findall(str(bsoup))
	
	print "+++++++++DEFENDANT+++++++++++++++"
	section_defendant = stable_table_address(sec_defendant, def_list)
	str_def = str(section_defendant[3]).replace('\n', ' ')
	section_defendant[3] = ' '.join(str_def.split())
	print section_defendant, '\n'
	
	print "**********CHARGES********************"
	section_charges = stable_table(sec_charges, charge_list)
	section_charges = handle_mult(section_charges, [], 5)
	print section_charges, '\n'
	
	print "+++++++++++++++++SENTENCE+++++++++++++++"
	section_sentence = stable_table(sec_sentence, sen_list)
	count_fields = 0
	for x in section_sentence:
		x = str(x).replace('\n', ' ')
		x = ' '.join(x.split())
		section_sentence[count_fields] = x
		count_fields += 1
		
	print section_sentence, '\n'
	
	print "+++++++++++++BONDS+++++++++++++++++++++"
	section_bonds = stable_table(sec_bonds, bonds_list)
	count_fields = 0
	for x in section_bonds:
		x = str(x).replace('\n', ' ')
		x = ' '.join(x.split())
		section_bonds[count_fields] = x
		count_fields += 1
	section_bonds = handle_mult(section_bonds, [], 4)
	print handle_mult(section_bonds, [], 4), '\n'
	
	print "+++++++++++++Case History+++++++++++++++++++++"
	section_casehist = stable_table(sec_casehist, case_list)
	section_casehist = handle_mult(section_casehist, [], 4)
	print handle_mult(section_casehist, [], 4), '\n'
		
	# i = 0
	# for x in section_casehist:
		# zero = section_casehist[i][0]
		# one = section_casehist[i][1]
		# two = section_casehist[i][2]
		# three = section_casehist[i][3]
		
		# zz += 1
	
	#Print Various Stuff From Soup:
	########################################################################################
	#for x in data_XLheader:
	#	print x
		
	# for x in data_medium:
		# for y in x.find_all("td"):
			# #print y.get_text(strip=True)
			# print y.get_text
	########################################################################################

	
	#Write final values in known order
	with criminal_out as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		
		try:
			#Is there more than once charge? Is there more than one bond? If more than one in both cases print.
			if len(section_charges) > 1:
				if len(section_bonds) < 1:
					print "More than one charge, One Bond"
					for entry in section_charges:
						writer.writerow([section_defendant[0], section_defendant[1], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14], entry[0], entry[1], entry[2], entry[3], entry[4], section_sentence[0], section_sentence[1], section_sentence[2], section_sentence[3], section_sentence[4], section_bonds[0][0], section_bonds[0][1], section_bonds[0][2], section_bonds[0][3], section_bonds[0][4]])
				else:
					print "More than one charge, More than One Bond"
					for entry in section_charges:
						for bond in section_bonds:
							#print count, "I HAVE 2 BONDS and 2 CHARGES!"
							#sys.exit()
							writer.writerow([section_defendant[0], section_defendant[1], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14], entry[0], entry[1], entry[2], entry[3], entry[4], section_sentence[0], section_sentence[1], section_sentence[2], section_sentence[3], section_sentence[4], bond[0], bond[1], bond[2], bond[3]])
			
			#There is only one charge... is there 2 bonds?			
			elif len(section_bonds) > 1:
				#print count, "I have 2 bonds!"
				#print section_bonds
				#print len(section_bonds)
				#sys.exit()
				print "I have more than one Bond"
				for entry in section_bonds:
					writer.writerow([section_defendant[0], section_defendant[1], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14], section_charges[0][0], section_charges[0][1], section_charges[0][2], section_charges[0][3], section_charges[0][4], section_sentence[0], section_sentence[1], section_sentence[2], section_sentence[3], section_sentence[4], entry[0], entry[1], entry[2], entry[3]])
			
			#Zero bonds print empty columns:
			elif len(section_bonds) < 1:
					print "Zero bonds print"
					writer.writerow([section_defendant[0], section_defendant[1], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14], section_charges[0][0], section_charges[0][1], section_charges[0][2], section_charges[0][3], section_charges[0][4], section_sentence[0], section_sentence[1], section_sentence[2], section_sentence[3], section_sentence[4], "", "", "", "", ""])
			
			#Only one charge, only one bond:
			else:
				print "Only one charge, only one bond"
				writer.writerow([section_defendant[0], section_defendant[1], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14], section_charges[0][0], section_charges[0][1], section_charges[0][2], section_charges[0][3], section_charges[0][4], section_sentence[0], section_sentence[1], section_sentence[2], section_sentence[3], section_sentence[4], section_bonds[0][0], section_bonds[0][1], section_bonds[0][2], section_bonds[0][3]])
		except:
			problems.append(count)
			
		
	return def_list, charge_list

#Double Charges case count test
#count = 169698

#Check ascii encoding error
#count = 303

while count < 1000000:
	print 'On Case #:', count
	criminal_out = open("criminal_out.csv", 'ab')
	#Request Page
	f = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(count))
	soup = BeautifulSoup(f.read())
	global problems
	problems = []
	#Storing the first b tag inside body to data_ccsort 
	data_ccsort = soup.body.b
	
	#If statement that sorts out civil cases 
	if data_ccsort.string == u'Civil Case View':
		print "Civil Case Continue..."
		count +=1
		print "ZZZZZZZ..."
		time.sleep(2.5)
	elif data_ccsort.string == 'Unable to load case data':
		print "Unable to load case data"
		count +=1
		print "ZZZZZZZ..."
		time.sleep(2.5)
	else:
		print "Criminal Case"
	
	#Run Parser Function here

		parse_gr(soup)
		count += 1
		print count
		time.sleep(2.5)
print problems, "Problem child?"
criminal_out.close()

	

	
	
	
########################################################################################
# Parse Robots:
# rp = robotparser.RobotFileParser()
# rp.set_url("http://neuro.compute.dtu.dk/robots.txt")
# rp.read()
# rp.can_fetch("*", "http://neuro.compute.dtu.dk/wiki/Special:Search")

# Mechanize Library #
# url = "http://www.grcourt.org/CourtPayments/loadCase.do?caseSequence=11"
# br = mechanize.Browser()
# #br.set_all_readonly(False)    # allow everything to be written to
# br.set_handle_robots(False)   # ignore robots
# br.set_handle_refresh(False)  # can sometimes hang without this
# br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]           # [('User-agent', 'Firefox')]
# response = br.open(url)
# print response.read()      # the text of the page
# response1 = br.response()  # get the response again
# print response1.read()     # can apply lxml.html.fromstring()

# user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
# headers = { 'JSESSIONID' : 'aaa1sKrRjU2bs7NGIotFu' }
# req = urllib2.Request("http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1", None, headers)
# response = urllib2.urlopen(req)
# page = response.read()