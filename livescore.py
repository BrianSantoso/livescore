import urllib3
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
# https://www.livescore18.com/
# https://www.livescore18.com/data/bf_en2.js?1548379839000
http = urllib3.PoolManager()
response = http.request('GET', 'https://www.livescore18.com/data/ft0_2.js?1548385046000')
soup = BeautifulSoup(response.data, 'lxml')

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

text = soup.getText()
lines = text.split("\n")
matchcountStart = findnth(text, '=', 3) + 1
matchcountEnd = findnth(text, ';', 3)
matchcount = text[matchcountStart:matchcountEnd]
matchcount = int(matchcount)
lines = lines[5:5+matchcount]

data = []
file = open('data.txt','w')


for line in lines:
	team1 = line[findnth(line, ',', 3):findnth(line, ',', 4)][2:-1]
	team2 = line[findnth(line, ',', 4):findnth(line, ',', 5)][2:-1]

	date = line[findnth(line, ',', 5):findnth(line, ',', 8)][2:].replace(',', '/')
	year = 0
	month = ''
	try:
		year = int(date[0:findnth(date, '/', 0)])
		month = date[findnth(date, '/', 0) + 1:findnth(date, '/', 1)]
		month = int(month) + 1
		month = str(month)
		if len(month) < 2:
			month = '0' + month
	except:
		print(line)
		continue


	
	
	day = date[findnth(date, '/', 1) + 1:]
	if len(day)<2:
		day = int('0' + day)
	day = int(day)


	time = line[findnth(line, ',', 8):findnth(line, ',', 10)][2:]
	hour = time[0:findnth(time, ',', 0)]
	minute = time[findnth(time, ',', 0) + 1:]
	timezone = line[findnth(line, ',', 17):findnth(line, ',', 18)][1:]
	timezone = int(timezone)
	# timezone_difference = 2 - (2 * timezone)
	timezone_difference = 2
	hour = str((int(hour) + timezone_difference))

	if len(hour) < 2:
		hour = '0' + hour


	finished = line[findnth(line, ',', 11):findnth(line, ',', 12)][1:]
	# print(finished)
	half = line[findnth(line, ',', 12):findnth(line, ',', 14)][1:].replace(',', '-')
	full = line[findnth(line, ',', 14):findnth(line, ',', 16)][1:].replace(',', '-')

	if finished == '-1':
		file.write(str(day) + '/' + str(month) + '/' + str(year) + '|' + hour + ':' + minute + '|' + team1 + ':' + team2 + '|' + half + '|' + full + '\n')

file.close()