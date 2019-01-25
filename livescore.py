import urllib3
import time as TIME
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime



# https://www.livescore18.com/
# https://www.livescore18.com/data/bf_en2.js?1548379839000
http = urllib3.PoolManager()
response = http.request('GET', 'https://www.livescore18.com/data/ft0_2.js')
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
file.truncate(0)

for line in lines:

	finished = line[findnth(line, ',', 11):findnth(line, ',', 12)][1:]
	if finished != '-1':
		continue

	team1 = line[findnth(line, ',', 3):findnth(line, ',', 4)][2:-1]
	team2 = line[findnth(line, ',', 4):findnth(line, ',', 5)][2:-1]

	date = line[findnth(line, ',', 5):findnth(line, ',', 8)][2:]
	year = month = 0

	year = int(date[0:findnth(date, ',', 0)])

	month = date[findnth(date, ',', 0) + 1:findnth(date, ',', 1)]
	month = int(month) + 1
	month = str(month)
	if len(month) < 2:
		month = '0' + month

	day = date[findnth(date, ',', 1) + 1:]
	if len(day) < 2:
		day = '0' + day
	day = int(day)


	time = line[findnth(line, ',', 8):findnth(line, ',', 10)][1:]
	minute = time[findnth(time, ',', 0) + 1:]

	timezone_difference = int(-TIME.timezone / 3600)
	hour = time[0:findnth(time, ',', 0)]
	hour = int(hour) + timezone_difference
	hour = hour % 24
	hour = str(hour)

	if len(hour) < 2:
		hour = '0' + hour
	
	half = line[findnth(line, ',', 12):findnth(line, ',', 14)][1:].replace(',', '-')
	full = line[findnth(line, ',', 14):findnth(line, ',', 16)][1:].replace(',', '-')

	data = str(day) + '/' + str(month) + '/' + str(year) + '|' + str(hour) + ':' + str(minute) + '|' + team1 + ':' + team2 + '|' + half + '|' + full + '\n'
	file.write(data)

file.close()